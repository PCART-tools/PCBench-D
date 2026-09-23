@register_decomposition(aten.dot)
@out_wrapper()
@_dot_check_wrapper
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self", "other"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def dot(self, other):
    if self.is_complex():
        if self.is_conj():
            if other.is_conj():
                return torch.dot(self.conj(), other.conj()).conj()
            else:
                return torch.vdot(self.conj(), other)
        elif other.is_conj():
            return torch.vdot(other.conj(), self)

    return (self * other).sum()
