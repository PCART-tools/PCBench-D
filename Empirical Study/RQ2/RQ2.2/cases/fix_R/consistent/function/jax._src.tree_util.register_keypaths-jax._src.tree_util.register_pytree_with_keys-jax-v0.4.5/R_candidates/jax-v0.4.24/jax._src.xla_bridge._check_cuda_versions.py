def _check_cuda_versions():
  assert cuda_versions is not None

  def _version_check(name, get_version, get_build_version,
                     scale_for_comparison=1):
    build_version = get_build_version()
    try:
      version = get_version()
    except Exception as e:
      raise RuntimeError(f"Unable to load {name}. Is it installed?") from e
    if build_version // scale_for_comparison > version // scale_for_comparison:
      raise RuntimeError(
          f"Found {name} version {version}, but JAX was built against version "
          f"{build_version}, which is newer. The copy of {name} that is "
          "installed must be at least as new as the version against which JAX "
          "was built."
      )

  _version_check("CUDA", cuda_versions.cuda_runtime_get_version,
                 cuda_versions.cuda_runtime_build_version)
  _version_check(
      "cuDNN",
      cuda_versions.cudnn_get_version,
      cuda_versions.cudnn_build_version,
      # NVIDIA promise both backwards and forwards compatibility for cuDNN patch
      # versions: https://docs.nvidia.com/deeplearning/cudnn/developer-guide/index.html#api-compat
      scale_for_comparison=100,
  )
  _version_check("cuFFT", cuda_versions.cufft_get_version,
                 cuda_versions.cufft_build_version,
                 # Ignore patch versions.
                 scale_for_comparison=100)
  _version_check("cuSOLVER", cuda_versions.cusolver_get_version,
                 cuda_versions.cusolver_build_version,
                 # Ignore patch versions.
                 scale_for_comparison=100)
  _version_check("cuPTI", cuda_versions.cupti_get_version,
                 cuda_versions.cupti_build_version)
  # TODO(jakevdp) remove these checks when minimum jaxlib is v0.4.21
  if hasattr(cuda_versions, "cublas_get_version"):
    _version_check("cuBLAS", cuda_versions.cublas_get_version,
                   cuda_versions.cublas_build_version,
                   # Ignore patch versions.
                   scale_for_comparison=100)
  if hasattr(cuda_versions, "cusparse_get_version"):
    _version_check("cuSPARSE", cuda_versions.cusparse_get_version,
                   cuda_versions.cusparse_build_version,
                   # Ignore patch versions.
                   scale_for_comparison=100)
