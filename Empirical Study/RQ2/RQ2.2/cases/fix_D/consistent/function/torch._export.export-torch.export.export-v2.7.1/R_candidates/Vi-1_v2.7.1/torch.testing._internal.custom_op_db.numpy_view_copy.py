@torch.library.custom_op("_torch_testing::numpy_view_copy", mutates_args=())
def numpy_view_copy(x: Tensor, shape: Sequence[int]) -> Tensor:
    return torch.tensor(np.copy(to_numpy(x).reshape(shape)), device=x.device)
