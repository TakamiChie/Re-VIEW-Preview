import threading
import argparse
from pathlib import Path

import webview

import js_api

APPNAME = "Re:VIEW Preview"
ev = threading.Event()
api = None

def get_args() -> argparse.Namespace:
  """
  Set Arguments
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("dir", help="Directory of Re:VIEW manuscript", type=str, nargs='?')
  return (parser.parse_args())

def load_thread(window: webview.Window, api) -> None:
  """
  Start work thread
  """
  with open(js_api.mypath() / "html" / "main.html", mode="r", encoding="utf-8") as f:
    html = ""
    mypath = js_api.path_to_url(js_api.mypath())
    for line in f:
      html += line.replace("..", mypath)
    webview.webview_ready()
    webview.load_html(html)
  api.update_title()
  api.update_list()

def main() -> None:
  args = get_args()
  api = js_api.JSAPI()
  window = webview.create_window(title=APPNAME, width=640, height=320, min_size=(360, 400), js_api=api)
  api.initialize(args.dir, window)
  webview.start(load_thread, args=(window, api), debug=True, http_server=True)

if __name__ == "__main__":
  main()