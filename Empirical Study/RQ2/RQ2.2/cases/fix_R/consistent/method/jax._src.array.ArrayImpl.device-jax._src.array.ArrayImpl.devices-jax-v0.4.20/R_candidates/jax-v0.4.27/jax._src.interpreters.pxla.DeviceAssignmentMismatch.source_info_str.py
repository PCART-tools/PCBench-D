  @property
  def source_info_str(self):
    return (
        "" if self.source_info is None
        else f" at {source_info_util.summarize(self.source_info.source_info)}"
    )
