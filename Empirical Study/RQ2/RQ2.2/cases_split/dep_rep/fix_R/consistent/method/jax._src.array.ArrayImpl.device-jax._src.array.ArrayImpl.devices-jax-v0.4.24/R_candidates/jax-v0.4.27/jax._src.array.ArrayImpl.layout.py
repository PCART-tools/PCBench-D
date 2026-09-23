  @property
  def layout(self):
    # TODO(yashkatariya): Remove the deleted check from here.
    if self.is_deleted():
      return Layout(None, self.sharding)
    try:
      return Layout(DeviceLocalLayout(self._pjrt_layout), self.sharding)
    except xe.XlaRuntimeError as e:
      msg, *_ = e.args
      if type(msg) is str and msg.startswith("UNIMPLEMENTED"):
        return Layout(None, self.sharding)
      else:
        raise
