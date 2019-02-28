import webview
import threading
import argparse
import js_api

APPNAME = "Re:VIEW Preview"
ev = threading.Event()
api = None

def get_args():
  """
  Set Arguments
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("dir", help="Directory of Re:VIEW manuscript", type=str)
  return (parser.parse_args())

def load_thread(args, api):
  """
  Start work thread
  """
  with open("html/main.html", mode="r", encoding="utf-8") as f:
    webview.load_html(f.read())
  api.update_title()
  api.update_list()

def main():
  args = get_args()
  if args.dir is not None:
    api = js_api.JSAPI(args.dir)
    threading.Thread(target=load_thread, args=(args, api)).start()
    webview.create_window(title=APPNAME, width=640, height=320, js_api=api)

if __name__ == "__main__":
  main()