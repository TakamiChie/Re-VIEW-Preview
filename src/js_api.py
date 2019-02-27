from pathlib import Path
import webview

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
      self.update_reviewfiles()

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

def update_dirname(dir):
  """
  Update the directory notation on the GUI.
  This method is called from the Python side.

  Parameter
  ----
  dir: str
    Directory of Re:VIEW manuscript.
  """
  webview.evaluate_js("document.getElementById('{0}').value = '{1}'".format("review-dir", dir))

