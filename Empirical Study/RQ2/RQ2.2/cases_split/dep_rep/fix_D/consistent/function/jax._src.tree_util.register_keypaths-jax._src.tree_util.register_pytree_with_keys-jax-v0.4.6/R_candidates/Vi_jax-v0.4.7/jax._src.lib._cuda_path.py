def _cuda_path() -> Optional[str]:
  _jaxlib_path = pathlib.Path(jaxlib.__file__).parent
  # If the pip package nvidia-cuda-nvcc-cu11 is installed, it should have
  # both of the things XLA looks for in the cuda path, namely bin/ptxas and
  # nvvm/libdevice/libdevice.10.bc
  path = _jaxlib_path.parent / "nvidia" / "cuda_nvcc"
  if path.is_dir():
    return str(path)
  # Failing that, we use the copy of libdevice.10.bc we include with jaxlib and
  # hope that the user has ptxas in their PATH.
  path = _jaxlib_path / "cuda"
  if path.is_dir():
    return str(path)
  return None
