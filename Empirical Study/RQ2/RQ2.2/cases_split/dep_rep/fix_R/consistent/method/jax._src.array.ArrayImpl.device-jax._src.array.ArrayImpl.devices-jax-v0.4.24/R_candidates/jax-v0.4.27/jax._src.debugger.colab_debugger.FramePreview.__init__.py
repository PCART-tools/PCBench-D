  def __init__(self, frame):
    super().__init__()
    self._header = colab_lib.dynamic(
        colab_lib.div(colab_lib.pre(colab_lib.code(""))))
    self._code_view = CodeViewer("", highlights=[])
    self.frame = frame
    self._file_cache = {}
