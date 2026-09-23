  def input_layouts(self):
    return [Layout(l, s)
            for l, s in safe_zip(self._in_layouts, self._in_shardings)]
