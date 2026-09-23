@torch.library.custom_op("_torch_testing::source4", mutates_args=())
def source4(x: Tensor) -> Tensor:
    return x.clone()
