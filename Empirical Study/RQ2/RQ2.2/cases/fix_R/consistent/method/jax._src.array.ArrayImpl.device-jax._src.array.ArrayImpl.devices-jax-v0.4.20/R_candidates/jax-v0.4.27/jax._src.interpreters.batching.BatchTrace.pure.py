  def pure(self, val):
    return BatchTracer(self, val, not_mapped, source_info_util.current())
