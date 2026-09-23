  def output_layouts(self):
    return [Layout(l, s)
            for l, s in safe_zip(self._out_layouts, self._out_shardings)]
