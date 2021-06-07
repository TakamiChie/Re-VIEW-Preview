import logging
from pathlib import Path
import typing
import js_api
import mimetypes

class Server:
  def __init__(self, logger: logging.Logger, api: js_api.JSAPI) -> None:
    self.__webview_url = ""
    self._jsapi = api
    self._logger = logger

  def __call__(self, environ: typing.Dict, start_response: typing.Callable) -> typing.Any:
    return self.proc(environ, start_response)

  def proc(self, environ: typing.Dict, start_response: typing.Callable) -> typing.Any:
    path = environ["PATH_INFO"]
    filepath = self.findfilepath(path)
    content = None
    headers = []
    status = ''
    if not filepath is None and filepath.exists():
      filetype, encoding = mimetypes.guess_type(filepath)
      with open(filepath, "rb") as f:
        content = f.read()
        status = '200 OK'
        headers = [('Content-type', f'{filetype}; charset=utf-8' if filetype.startswith("text") else filetype)]
    else:
      status = '404 Not found'
      content= b'Not found'
    self._logger.debug(f"status:{status} {path}->{filepath} Content Size:{len(content)}")
    start_response(status, headers)
    return [content]

  def findfilepath(self, path: str) -> Path:
    """
    Convert requested path information into actual path information.

    Parameters
    ----
    path: str
      path.Environment variable PATH_INFO value.

    Returns
    ----
    path: pathlib.Path
      Actual file path.
    """
    if path == "/":
      # main.html
      return js_api.mypath() / "html" / "main.html"
    elif path.startswith("/node_modules") or path.startswith("/html"):
      # Other files owned by the application.
      return js_api.mypath() / path[1:]
    elif path.startswith("/appicon"):
      return js_api.mypath() / path[1:]
    elif path.startswith("/favicon.ico"):
      return js_api.mypath() / "appicon.ico"
    elif path.startswith("/book"):
      return self._jsapi._review_dir / '/'.join(path.split("/")[2:])
    else:
      return None

