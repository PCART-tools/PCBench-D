@register_meta(
    [
        aten.mul_.Scalar,
        aten.div_.Scalar,
        aten.mul_.Tensor,
        aten.div_.Tensor,
        aten.logical_and_.default,
        aten.logical_or_.default,
        aten.logical_xor_.default,
    ],
)
def meta_binop_inplace(self, other):
    if isinstance(other, torch.Tensor):
        check_inplace_broadcast(self.shape, other.shape)
    return self
