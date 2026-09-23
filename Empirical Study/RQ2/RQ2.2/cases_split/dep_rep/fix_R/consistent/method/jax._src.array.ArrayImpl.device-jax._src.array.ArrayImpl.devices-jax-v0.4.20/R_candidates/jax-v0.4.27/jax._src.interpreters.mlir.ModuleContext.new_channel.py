  def new_channel(self) -> int:
    return next(self.channel_iterator)
