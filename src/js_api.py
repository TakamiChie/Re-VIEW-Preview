from pathlib import Path
import webview

from executor import Executor

import main

class JSAPI:
  """
  JSAPI
  """
  def __init__(self, review_dir):
    """
    Initialize Object.

    Parameters
    ----
    review_dir: str
      Directory of Re:VIEW manuscript.
    """
    self.executor = Executor()
    self.executor.findreview()
    self.change_review_dir(review_dir, guiupdate=False)

  def change_review_dir(self, dir, guiupdate=True):
    """
    Change Re:VIEW's directory

    Parameters
    ----
    dir: str
      Directory of Re:VIEW manuscript.
    guiupdate: bool
      Specify true if GUI updates are performed at the same time (default true).
    """
    self._review_dir = Path(dir)
    self._files = list(self._review_dir.glob("*.re"))
    if guiupdate:
      self.update_title()
      self.update_list()

  def update_title(self):
    """
    Update GUI Window title.
    """
    webview.set_title("{0} - {1}".format(main.APPNAME, self._review_dir.stem))

  def update_list(self):
    """
    Update GUI file list.
    """
    js = """
    combo = document.getElementById('review-file');
    while(combo.length > 0){ combo.remove(0); }
    """
    for file in self._files:
      js += """
      {{
        let op = document.createElement("option");
        op.value = "{0}";
        op.text = "{0}";
        combo.appendChild(op);
      }}
      """.format(file.name)
    webview.evaluate_js(js)
    self.show_review(self._files[0])

  def show_review(self, filename = None):
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
    if filename is None:
      pass
    elif Path(filename).is_absolute():
      self._review_file = filename
    else:
      self._review_file = self._review_dir / filename
    webview.evaluate_js("document.getElementById('preview_frame').src = '{0}';".format(self._path_to_url(mypath() / "html" / "loading.html")))
    reviewtxt = self.executor.compile(self._review_file)
    previewhtml = self._review_file.parent / "preview.html"
    with open(previewhtml, mode="w", encoding="utf-8") as f:
      f.write(reviewtxt)
    webview.evaluate_js("document.getElementById('preview_frame').src = '{0}';".format(self._path_to_url((previewhtml))))

  def _path_to_url(self, path):
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

def mypath():
  """
  Get the root folder path for the project.

  Returns
  ----
  path: Path
    Root folder path for the project.
  """
  import sys
  return Path(sys.argv[0]) if hasattr(sys, "frozen") else \
    Path(__file__).parent.parent
