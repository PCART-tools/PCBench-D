@functools.lru_cache(8)
def _normalize_cuda_arch(arch: str) -> str:
    if int(arch) >= 100:
        log.warning(
            "Detected CUDA architecture >= 100: %s. We will generate operations with "
            "GenerateSM100 (if available) and GenerateSM90. Please file an "
            "issue for any problems and feedback. ",
            arch,
        )

    if int(arch) >= 100:
        return "100"
    elif int(arch) >= 90:
        return "90"
    elif int(arch) >= 80:
        return "80"
    elif int(arch) >= 75:
        return "75"
    elif int(arch) >= 70:
        return "70"
    else:
        raise NotImplementedError(f"Unsupported cuda arch: {arch}")
