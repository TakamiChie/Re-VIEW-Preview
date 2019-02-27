from subprocess import Popen, PIPE
from chardet import detect

class Executor:
  """
  Executor of Re:VIEW
  """
  def __init__(self):
    """
    Initialize
    """
    self.findreview()

  def findreview(self):
    """
    Find review command.
    """
    try:
      self._review_path = self.call(["where", "review"]).split("\r\n")[0]
    except FileNotFoundError:
      self._review_path = None
    return self._review_path

  def call(self, args):
    """
    Execute the external program and obtain the result.

    Paraneters
    ----
    args: list(str)
      Arguments.

    Returns
    ----
    return: str
      stdout.

    Errors
    ----
    ValueError: str
      stderr was output.
    """
    out, err = Popen(args, stdout=PIPE,
      stderr=PIPE).communicate()

    if err != b"":
      raise ValueError(err.decode(detect(err)["encoding"]))
    return out.decode(detect(out)["encoding"])

  def compile(self, filepath):
    """
    Execute Re:VIEW converter.

    Parameters
    ----
    filepath: str or Path
      File path to be converted
    """
    if self._review_path is not None:
      out = self.call([self._review_path,
        "compile",
        "--target", "html",
        filepath])
      return out

if __name__ == "__main__":
  exec = Executor()
  try:
    exec.call(["unknown"])
  except FileNotFoundError:
    print("Test OK")
  try:
    exec.call(["where", "unknown"])
  except ValueError as e:
    print("Test OK")
    print(e)
  print(exec.findreview())
  print(exec.compile("../testbook/testbook.re"))