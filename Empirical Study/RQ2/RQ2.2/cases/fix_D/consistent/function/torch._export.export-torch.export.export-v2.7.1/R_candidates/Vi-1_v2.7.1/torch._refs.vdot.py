@register_decomposition(aten.vdot)
@out_wrapper()
@_dot_check_wrapper
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self", "other"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def vdot(self, other):
    if not self.is_complex():
        return torch.dot(self, other)

    if self.is_conj():
        if other.is_conj():
            return torch.vdot(other.conj(), self.conj())
        else:
            return torch.dot(self.conj(), other)
    elif other.is_conj():
        return torch.dot(self, other.conj()).conj()

    # The decomposition fails if you do self.conj()... not sure why
    return (self.conj_physical() * other).sum()
