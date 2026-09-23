def _suggest_missing_backends():
  if py_platform.system() != "Linux":
    # If you're not using Linux (or WSL2), we don't have any suggestions at the
    # moment.
    return

  assert _default_backend is not None
  default_platform = _default_backend.platform
  nvidia_gpu_devices = [
    "/dev/nvidia0",
    "/dev/dxg",  # WSL2
  ]
  if ("cuda" not in _backends and
      any(os.path.exists(d) for d in nvidia_gpu_devices)):
    if hasattr(xla_extension, "GpuAllocatorConfig") and "cuda" in _backend_errors:
      err = _backend_errors["cuda"]
      logger.warning(f"CUDA backend failed to initialize: {err} (Set "
                     "TF_CPP_MIN_LOG_LEVEL=0 and rerun for more info.)")
    else:
      logger.warning("An NVIDIA GPU may be present on this machine, but a "
                     "CUDA-enabled jaxlib is not installed. Falling back to "
                     f"{default_platform}.")
  elif "tpu" not in _backends and hardware_utils.num_available_tpu_chips_and_device_id()[0] > 0:
    logger.warning("A Google TPU may be present on this machine, but either a "
                    "TPU-enabled jaxlib or libtpu is not installed. Falling "
                    f"back to {default_platform}.")
