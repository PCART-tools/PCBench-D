def _get_cpp_prefix_header(device: str) -> Optional[str]:
    if device.startswith("cpu"):
        return "torch/csrc/inductor/cpp_prefix.h"
    return None
