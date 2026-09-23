@_make_elementwise_unary_reference(ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT)
def sinc(a):
    a = math.pi * a
    return torch.where(a == 0, 1, torch.sin(a) / a)
