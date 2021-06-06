import typing

import webview

class WebViewCommunicator:
  """
  Methods for retrieving and setting WebView values.
  """

  # window properties.

  @property
  def title(self) -> str:
    """
    Gets and sets the title of the window.
    """
    return webview.evaluate_js("document.title")

  @title.setter
  def title(self, newtitle: str) -> None:
    """
    Gets and sets the title of the window.
    """
    return webview.set_title(newtitle)

  @property
  def frameurl(self) -> str:
    """
    Gets and sets the URL of the iframe#preview_frame.
    """
    return webview.evaluate_js("document.getElementById('preview_frame').src")

  @frameurl.setter
  def frameurl(self, url: str) -> None:
    """
    Gets and sets the URL of the iframe#preview_frame.
    """
    webview.evaluate_js("document.getElementById('preview_frame').src = '{0}';".format(url))

  # methods.

  def showmsg(self, title: str, message: str) -> None:
    """
    Displays a toast message.

    Parameters
    ----
    title: str
      Toast title.
    message: str
      Toast message.
    """
    js = """
    document.getElementById("msg_output_header").innerText = "{0}";
    document.getElementById("msg_output_body").innerText = "{1}";
    $("#msg_output").toast("show");
    """.format(title, str(message).replace("\r\n", ""))
    webview.evaluate_js(js)

  def setfilelist(self, files: typing.List[str]) -> None:
    """
    Update select#review-file.

    Parameters
    ----
    files: str[list]
      File lists.
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
