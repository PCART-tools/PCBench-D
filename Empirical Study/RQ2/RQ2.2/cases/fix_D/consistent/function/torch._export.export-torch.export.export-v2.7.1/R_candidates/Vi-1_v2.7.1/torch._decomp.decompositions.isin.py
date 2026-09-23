@register_decomposition(aten.isin)
@out_wrapper()
def isin(elements, test_elements, *, assume_unique=False, invert=False):
    # handle when either elements or test_elements are Scalars (they can't both be)
    if not isinstance(elements, torch.Tensor):
        elements = torch.tensor(elements, device=test_elements.device)
    if not isinstance(test_elements, torch.Tensor):
        if invert:
            return torch.ne(elements, test_elements)
        else:
            return torch.eq(elements, test_elements)

    if test_elements.numel() < 10.0 * pow(elements.numel(), 0.145):
        return isin_default(elements, test_elements, invert=invert)
    else:
        return isin_sorting(
            elements, test_elements, assume_unique=assume_unique, invert=invert
        )
