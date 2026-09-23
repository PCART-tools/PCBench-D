@clear_on_fresh_cache
@functools.lru_cache(1)
def get_cuda_arch() -> Optional[str]:
    try:
        cuda_arch = config.cuda.arch
        if cuda_arch is None:
            # Get Compute Capability of the first Visible device
            major, minor = torch.cuda.get_device_capability(0)
            return str(major * 10 + minor)
        return str(cuda_arch)
    except Exception as e:
        log.error("Error getting cuda arch: %s", e)
        return None
