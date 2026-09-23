def isin_default(elements, test_elements, *, invert=False):
    if elements.numel() == 0:
        return torch.empty_like(elements, dtype=torch.bool)
    x = elements.view(*elements.shape, *((1,) * test_elements.ndim))
    dim = tuple(range(-1, -test_elements.ndim - 1, -1))
    res = (x == test_elements).any(dim=dim)
    return ~res if invert else res
