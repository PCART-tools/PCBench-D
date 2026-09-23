  def __init__(self, code_: str, highlights: list[int], linenostart: int = 1):
    self._code = code_
    self._highlights = highlights
    self._view = colab_lib.dynamic(colab_lib.div())
    self._linenostart = linenostart
