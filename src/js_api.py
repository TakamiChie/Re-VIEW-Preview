from pathlib import Path
import webview
import typing
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from executor import Executor
from wvcomm import WebViewCommunicator

import const

class ChangeHandler(FileSystemEventHandler):
  """
  Event handlers for watchdog.
  """

  def __init__(self, owner):
    """
    Initialize

    Parameters
    ----
    owner: JSAPI
      owner object.
    """
    self.owner = owner
    self.lastfile = { "name": "", "time": 0}

  def on_created(self, event):
    return

  def on_modified(self, event):
    """
    An event handler that is invoked when it detects that a file has been modified.

    Reload the file only when you are updating the currently displayed file.

    Note that in Windows on_modified() occurs twice.

    It is permissible to call the show_review() twice in succession because it may be a case that
    is not called in succession twice by the environment that the defect
    does not occur even if it calls show_review() twice in succession.
    """
    p = Path(event.src_path)
    if (p == self.owner._review_file or p.suffix in [".js", ".css"]) and \
      (p.name != self.lastfile["name"] or p.stat().st_mtime != self.lastfile["time"]):
      self.lastfile = {
        "name": p.name,
        "time": p.stat().st_mtime
      }
      self.owner.show_review()

  def on_deleted(self, event):
    return

class JSAPI:
  """
  JSAPI
  """
  def __init__(self) -> None:
    """
    Initialize Object.
    """
    self.executor = Executor()
    self.executor.findreview()
    self._comm = None
    self.observer = None
    self._review_file = None
    self._review_dir = None
    self._files = None

  def initialize(self, review_dir: str, window: webview.Window) -> None:
    """
    Initialize Object 2.
    PyWebView upgrade separates it from constructors because it requires window objects to connect to WebView.
    You must always call this method before calling it.

    Parameters
    ----
    review_dir: str|None
      Directory of Re:VIEW manuscript.
    window: webview.Window
      WebView Window Object.
    """
    self._comm = WebViewCommunicator(window)
    if review_dir is not None:
      self.change_review_dir(review_dir, guiupdate=False)

  def change_review_dir(self, dir: str, guiupdate: bool=True) -> None:
    """
    Change Re:VIEW's directory

    Parameters
    ----
    dir: str
      Directory of Re:VIEW manuscript.
    guiupdate: bool
      Specify true if GUI updates are performed at the same time (default true).
    """
    if self.observer is not None:
      self.observer.stop()
      self.observer.join()
      self.observer = None
    self._review_dir = Path(dir)
    self._files = list(self._review_dir.glob("*.re"))
    if guiupdate:
      self.update_title()
      self.update_list()
    self.observer = Observer()
    self.observer.schedule(ChangeHandler(self), str(self._review_dir))
    self.observer.start()

  def update_title(self) -> None:
    """
    Update GUI Window title.
    """
    if self._review_dir is None:
      self._comm.title = const.APPNAME
    else:
      self._comm.title = "{0} - {1}".format(const.APPNAME, self._review_dir.stem)

  def update_list(self) -> None:
    """
    Update GUI file list.
    """
    if self._review_dir is not None:
      self._comm.setfilelist(self._files)
      self.show_review(self._files[0])

  def show_review(self, filename: typing.Union[str,Path] = None) -> None:
    """
    Update GUI Re:VIEW window.

    Parameters
    ----
    filename: str or Path or None
      The file path of the file to preview.
      If the argument is a relative path,
      it is considered to be a relative path from review_dir.
      If the argument is none, only the current file is reloaded.
    """
    pos = 0
    if filename is None:
      pos = self._comm.evaluate_js("pos")
    elif Path(filename).is_absolute():
      self._review_file = filename
    else:
      self._review_file = self._review_dir / filename
    self._comm.frameurl = "/html/loading.html"
    if self._review_file != None:
      previewhtml = self._review_file.parent / "preview.html"
      try:
        reviewtxt = self.executor.compile(self._review_file)
        with open(previewhtml, mode="w", encoding="utf-8") as f:
          f.write(reviewtxt.replace("</body>",
            "<script src='/html/frame.js'></script></body>") \
              .replace("</head>",
              "<link rel='stylesheet' href='/html/frame.css'></head>")
              )
      except ValueError as e:
        self._comm.showmsg("Error", e)
      finally:
        self._comm.frameurl = "/book/preview.html?{0}#top{1}".format(self._review_file.stem, pos)

  def directory_open(self, params: typing.Any = None) -> None:
    """
    Display a dialog and change the Re:VIEW directory.

    Parameters
    ----
    params: None
      Unused.
    """
    dir = self._comm.window.create_file_dialog(webview.FOLDER_DIALOG,
      directory=str(self._review_dir) or '',
      allow_multiple=False)
    self.change_review_dir(dir[0])

def path_to_url(path: Path) -> str:
  """
  Convert the file path to a URL that can be embedded in JavaScript.

  Parameters
  ----
  path: Path
    Path

  Returns
  ----
  url: str
    URL
  """
  return str(path).replace("\\", "\\\\")

def mypath() -> Path:
  """
  Get the root folder path for the project.

  Returns
  ----
  path: Path
    Root folder path for the project.
  """
  import sys
  return Path(sys.prefix) if hasattr(sys, "frozen") else \
    Path(__file__).parent.parent
