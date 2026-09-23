@aten.tensor_split.tensor_indices_or_sections.py_impl(
    DispatchKey.CompositeImplicitAutograd
)
def tensor_split_tensor_indices_or_sections_py_impl(
    self: Tensor,
    tensor_indices_or_sections: Tensor,
    dim: int = 0,
) -> tuple[Tensor, ...]:
    assert tensor_indices_or_sections.device.type == "cpu"
    assert tensor_indices_or_sections.dtype == torch.int64
    split_dim = tensor_indices_or_sections.dim()
    torch._check(
        split_dim == 1 or split_dim == 0,
        lambda: "tensor_split expected tensor_indices_or_sections to be a zero-dimensional "
        f"or one-dimensional tensor, but got a tensor with {split_dim} dims",
    )
    if split_dim == 0:
        sections = tensor_indices_or_sections.item()
        assert isinstance(sections, IntLike)
        return self.tensor_split(sections, dim)
    else:
        indices = [i.item() for i in tensor_indices_or_sections]
        # WARNING: Tempted to torch._check_is_size on the indices here?  You
        # can't: tensor_split works with negative values in indices:
        #
        # >>> torch.tensor_split(torch.randn(10), torch.tensor([-5, 5]))
        # (tensor([ 0.3540,  2.1074, -0.8507,  1.1639,  0.3055]), tensor([]),
        # tensor([-0.4285,  1.0692, -0.1776,  0.9362,  1.6143]))
        #
        # Sorry, I don't make the rules.  Explicitly do the item call in user
        # code if you KNOW that they are non-negative.
        return self.tensor_split(indices, dim)
