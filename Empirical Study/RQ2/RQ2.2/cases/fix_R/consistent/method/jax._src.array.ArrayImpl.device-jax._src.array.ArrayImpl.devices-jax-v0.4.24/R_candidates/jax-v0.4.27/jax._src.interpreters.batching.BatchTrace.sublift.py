  def sublift(self, val):
    return BatchTracer(self, val.val, val.batch_dim, source_info_util.current())
