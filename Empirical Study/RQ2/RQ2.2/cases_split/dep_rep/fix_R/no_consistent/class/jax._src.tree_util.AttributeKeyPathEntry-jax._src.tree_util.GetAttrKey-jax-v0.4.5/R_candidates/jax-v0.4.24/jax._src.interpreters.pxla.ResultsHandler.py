class ResultsHandler:
  # `out_avals` is the `Array` global avals when using pjit or xmap
  # with `config.parallel_functions_output_gda=True`. It is the local one
  # otherwise, and also when using `pmap`.
  __slots__ = ("handlers", "out_shardings", "out_avals")

  def __init__(self, handlers, out_shardings, out_avals):
    self.handlers = handlers
    self.out_shardings = out_shardings
    self.out_avals = out_avals

  def __call__(self, out_bufs):
    return [h(bufs) for h, bufs in safe_zip(self.handlers, out_bufs)]
