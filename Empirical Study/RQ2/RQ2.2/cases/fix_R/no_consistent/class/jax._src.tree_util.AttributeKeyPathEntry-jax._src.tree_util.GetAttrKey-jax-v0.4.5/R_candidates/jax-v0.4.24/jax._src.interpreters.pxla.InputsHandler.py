class InputsHandler:
  __slots__ = ("handler", "local_devices", "in_shardings", "input_indices")

  def __init__(self, in_shardings, local_devices=None, input_indices=None):
    self.handler = partial(shard_args, in_shardings)
    self.local_devices = local_devices
    self.in_shardings = in_shardings
    self.input_indices = input_indices

  def __call__(self, input_buffers):
    return self.handler(input_buffers)

  def __str__(self):
    return ("InputsHandler(\n"
            f"local_devices={self.local_devices},\n"
            f"in_shardings={self.in_shardings},\n"
            f"input_indices={self.input_indices})")
