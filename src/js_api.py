from pathlib import Path
import webview

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
      let op = document.createElement("option");
      op.value = "{0}";
      op.text = "{0}";
      combo.appendChild(op);
      """.format(file.name)
    webview.evaluate_js(js)
    self.show_review(self._files[0])

  def show_review(self, filename):
    """
    Update GUI Re:VIEW window.
    """
    self._review_file = filename

