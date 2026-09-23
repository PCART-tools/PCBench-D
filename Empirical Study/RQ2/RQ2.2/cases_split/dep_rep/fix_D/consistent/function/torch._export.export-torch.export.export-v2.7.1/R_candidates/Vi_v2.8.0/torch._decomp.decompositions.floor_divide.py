@register_decomposition(aten.floor_divide)
@out_wrapper()
def floor_divide(self, other):
    return torch.div(self, other, rounding_mode="floor")
