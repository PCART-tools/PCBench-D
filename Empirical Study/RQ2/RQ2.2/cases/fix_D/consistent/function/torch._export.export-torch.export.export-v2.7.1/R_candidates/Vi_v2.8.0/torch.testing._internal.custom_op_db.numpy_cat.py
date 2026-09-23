@torch.library.custom_op('_torch_testing::numpy_cat', mutates_args=())
def numpy_cat(xs: Sequence[Tensor], dim: int) -> Tensor:
    assert len(xs) > 0
    assert all(x.device == xs[0].device for x in xs)
    assert all(x.dtype == xs[0].dtype for x in xs)
    np_xs = [to_numpy(x) for x in xs]
    np_out = np.concatenate(np_xs, axis=dim)
    return torch.tensor(np_out, device=xs[0].device)
