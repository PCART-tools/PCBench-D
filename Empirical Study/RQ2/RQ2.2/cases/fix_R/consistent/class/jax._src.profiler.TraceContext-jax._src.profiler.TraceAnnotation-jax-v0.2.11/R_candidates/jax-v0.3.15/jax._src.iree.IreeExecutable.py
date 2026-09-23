class IreeExecutable:

  def __init__(self, client, devices, module_object, function_name):
    self.client = client
    self.traceback = None
    self.fingerprint = None
    self._devices = devices
    self.module_object = module_object
    self.function_name = function_name

  def local_devices(self) -> List[IreeDevice]:
    return self._devices

  def execute(self, arguments: Sequence[IreeBuffer]) -> List[IreeBuffer]:
    inputs = [arg.to_iree() for arg in arguments]
    outputs = self.module_object[self.function_name](*inputs)
    # TODO(phawkins): Have a way to just have it always return the list,
    # regardless of arity.
    if not isinstance(outputs, list) and not isinstance(outputs, tuple):
      outputs = [outputs]
    return [
        IreeBuffer(self.client, self._devices[0], output) for output in outputs
    ]
