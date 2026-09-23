  def __init__(self, in_shardings, local_devices=None, input_indices=None):
    self.handler = partial(shard_args, in_shardings)
    self.local_devices = local_devices
    self.in_shardings = in_shardings
    self.input_indices = input_indices
