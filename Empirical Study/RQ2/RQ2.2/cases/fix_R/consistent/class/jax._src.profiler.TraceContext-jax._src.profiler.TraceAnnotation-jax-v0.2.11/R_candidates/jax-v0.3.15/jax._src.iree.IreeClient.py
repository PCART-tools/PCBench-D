class IreeClient:

  def __init__(self,
               *,
               iree_backend: str = None):
    self.platform = "iree"
    self.platform_version = "0.0.1"
    self.runtime_type = "iree"
    self.iree_backend = (FLAGS.jax_iree_backend if iree_backend is None
                        else iree_backend)
    self.compiler_driver = iree_compiler_map[self.iree_backend]
    self.runtime_driver = iree_runtime_map[self.iree_backend]
    self.iree_config = iree.runtime.system_api.Config(self.runtime_driver)
    self._devices = [IreeDevice(self)]

  def process_index(self) -> int:
    return 0

  def device_count(self) -> int:
    return len(self._devices)

  def devices(self) -> List[IreeDevice]:
    return self._devices

  def local_devices(self) -> List[IreeDevice]:
    return self._devices

  def local_device_count(self) -> int:
    return len(self._devices)

  def get_default_device_assignment(
      self,
      num_replicas: int) -> List[IreeDevice]:
    if num_replicas != 1:
      raise NotImplementedError("Only single-device computations implemented")
    return [self._devices[0]]


  def compile(self, computation: str,
              compile_options: xla_client.CompileOptions) -> IreeExecutable:
    del compile_options  # Ignored.
    extra_args = []
    # extra_args=["--mlir-print-ir-after-all"]
    if platform.system() == "Darwin" and platform.machine() == "arm64":
      extra_args += ["--iree-llvm-target-triple=arm64-apple-darwin21.5.0"]
    iree_binary = iree.compiler.compile_str(
        computation, target_backends=[self.compiler_driver], input_type="mhlo",
        # extended_diagnostics=True,
        extra_args=extra_args,
    )
    # Load it into the runtime.
    vm_module = iree.runtime.VmModule.from_flatbuffer(iree_binary)
    module_object = iree.runtime.load_vm_module(vm_module, self.iree_config)
    return IreeExecutable(self, self._devices, module_object, "main")

  def buffer_from_pyval(
      self,
      argument: Any,
      device: Optional[IreeDevice],
      force_copy: bool = True,
      host_buffer_semantics: xla_client.HostBufferSemantics = xla_client
      .HostBufferSemantics.ZERO_COPY
  ) -> IreeBuffer:
    # TODO(phawkins): IREE's python API will accept a numpy array directly but
    # may want to explicitly construct a lower level BufferView to avoid copies.
    if device is None:
      assert type(argument) is np.ndarray
      device = self._devices[0]
    return IreeBuffer(self, device, np.array(argument, copy=True))
