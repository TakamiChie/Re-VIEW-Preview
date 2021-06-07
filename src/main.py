import threading
import argparse
import logging
import json
from pathlib import Path

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
    self.config = {
      "window": {}
    }
    if (js_api.mypath() / "config.json").exists():
      with open(js_api.mypath() / "config.json", "r") as f:
        self.config.update(json.load(f))

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

    self.window = webview.create_window(const.APPNAME, self.server,
      width = self.config["window"]["width"] if "width" in self.config["window"] else 640,
      height =  self.config["window"]["height"] if "height" in self.config["window"] else 320,
      min_size = (360, 400), js_api=api)
    if "x" in self.config["window"]: self.window.initial_x = self.config["window"]["x"]
    if "y" in self.config["window"]: self.window.initial_y = self.config["window"]["y"]
    if "openeddir" in self.config and self.args.dir is None and Path(self.config["openeddir"]).exists() :
      self.args.dir = self.config["openeddir"]

    self.window.closing += self.onclosing
    self.api.initialize(self.args.dir, self.window)
    webview.start(self.load_thread, args=(self.window, self.api), debug=True)

  def onclosing(self):
    self.config["window"]["x"] = self.window.x
    self.config["window"]["y"] = self.window.y
    self.config["window"]["width"] = self.window.width
    self.config["window"]["height"] = self.window.height
    self.config["openeddir"] = str(self.api._review_dir)
    with open(js_api.mypath() / "config.json", "w") as f:
      json.dump(self.config, f, indent=2)

if __name__ == "__main__":
  Application().main()