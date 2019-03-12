import webview

class WebViewCommunicator:
  """
  Methods for retrieving and setting WebView values.
  """

  # window properties.

  @property
  def title(self):
    """
    Gets and sets the title of the window.
    """
    return webview.evaluate_js("document.title")

  @title.setter
  def title(self, newtitle):
    """
    Gets and sets the title of the window.
    """
    return webview.set_title(newtitle)

  @property
  def frameurl(self):
    """
    Gets and sets the URL of the iframe#preview_frame.
    """
    return webview.evaluate_js("document.getElementById('preview_frame').src")

  @frameurl.setter
  def frameurl(self, url):
    """
    Gets and sets the URL of the iframe#preview_frame.
    """
    webview.evaluate_js("document.getElementById('preview_frame').src = '{0}';".format(url))

  # methods.
  def setfilelist(self, files):
    """
    Update select#review-file.
    """
    js = """
    combo = document.getElementById('review-file');
    while(combo.length > 0){ combo.remove(0); }
    """
    for file in files:
      js += """
      {{
        let op = document.createElement("option");
        op.value = "{0}";
        op.text = "{0}";
        combo.appendChild(op);
      }}
      """.format(file.name)
    webview.evaluate_js(js)
