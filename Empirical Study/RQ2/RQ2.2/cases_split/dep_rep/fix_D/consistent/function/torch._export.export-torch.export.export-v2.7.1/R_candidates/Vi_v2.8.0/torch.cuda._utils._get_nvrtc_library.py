def _get_nvrtc_library() -> ctypes.CDLL:
    # Since PyTorch already loads NVRTC, we can use the system library
    # which should be compatible with PyTorch's version
    if sys.platform == "win32":
        return ctypes.CDLL("nvrtc64_120_0.dll")
    else:
        return ctypes.CDLL("libnvrtc.so")
