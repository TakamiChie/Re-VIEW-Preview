import threading
import argparse
import logging

import webview

import js_api
import server
import const

ev = threading.Event()
api = None

class Application:

  def __init__(self) -> None:
    self.args = self.get_args()
    self.api = js_api.JSAPI()
    self.log = logging.getLogger(const.APPNAME)
    self.log.setLevel(logging.DEBUG)
    self.log.addHandler(logging.StreamHandler())

  def get_args(self) -> argparse.Namespace:
    """
    Set Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Directory of Re:VIEW manuscript", type=str, nargs='?')
    return (parser.parse_args())

  def load_thread(self, window: webview.Window, api) -> None:
    """
    Start work thread
    """
    api.update_title()
    api.update_list()

  def main(self) -> None:
    self.server = server.Server(logger=self.log.getChild(server.Server.__name__), api=self.api)
    self.window = webview.create_window(const.APPNAME, self.server, width=640, height=320, min_size=(360, 400), js_api=api)
    self.api.initialize(self.args.dir, self.window)
    webview.start(self.load_thread, args=(self.window, self.api), debug=True)

if __name__ == "__main__":
  Application().main()