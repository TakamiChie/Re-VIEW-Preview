import threading
import argparse
import logging

import webview

import js_api
import server
import const

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
  api.update_title()
  api.update_list()

def main() -> None:
  args = get_args()
  api = js_api.JSAPI()
  log = logging.getLogger(const.APPNAME)
  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  serv = server.Server(logger=log.getChild(server.Server.__name__), api=api)
  window = webview.create_window(const.APPNAME, serv, width=640, height=320, min_size=(360, 400), js_api=api)
  api.initialize(args.dir, window)
  webview.start(load_thread, args=(window, api), debug=True)

if __name__ == "__main__":
  main()