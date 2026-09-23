@torch.library.impl(lib, "copy_", "Meta")
@torch.library.impl(lib, "copy_", "CUDA")
@torch.library.impl(lib, "copy_", "XPU")
@torch.library.impl(lib, "copy_", "HPU")
@torch.library.impl(lib, "copy_", "CPU")
@torch.library.impl(lib, "copy_", "MTIA")
def copy_(tensor, data):
    tensor.copy_(data)
