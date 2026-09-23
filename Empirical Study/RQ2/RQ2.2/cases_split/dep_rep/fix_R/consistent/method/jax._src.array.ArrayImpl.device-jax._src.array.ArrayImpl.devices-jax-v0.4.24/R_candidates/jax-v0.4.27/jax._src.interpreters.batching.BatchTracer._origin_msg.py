  def _origin_msg(self):
    if self.source_info is None:
      return ""
    return (f"\nThis BatchTracer with object id {id(self)} was created on line:"
            f"\n  {source_info_util.summarize(self.source_info)}")
