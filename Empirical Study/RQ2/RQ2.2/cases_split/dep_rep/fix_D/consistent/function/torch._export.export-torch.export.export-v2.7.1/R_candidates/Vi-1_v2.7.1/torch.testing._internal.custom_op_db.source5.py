@torch.library.custom_op("_torch_testing::source5", mutates_args=())
def source5(x: Tensor) -> Tensor:
    return x.clone()
