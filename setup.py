import shutil
import subprocess
from pathlib import Path

print("> Setup TestBook")
if not Path("testbook").exists():
  subprocess.call("review init testbook", shell=True)

print("> Copy Data")
for f in Path("re_files").glob("*"):
  shutil.copy(f.absolute(), "testbook")

print("Finished!")