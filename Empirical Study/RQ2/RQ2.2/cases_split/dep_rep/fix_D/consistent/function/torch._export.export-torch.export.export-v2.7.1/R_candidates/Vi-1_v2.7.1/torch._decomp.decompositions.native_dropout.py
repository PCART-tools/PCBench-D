@register_decomposition(aten.native_dropout)
@out_wrapper("out0", "out1")
def native_dropout(input: Tensor, p: float, train: Optional[bool]):
    if train and p != 0:
        if p == 1:
            return (torch.zeros_like(input), torch.zeros_like(input, dtype=torch.bool))
        if not input.dtype.is_floating_point:
            raise RuntimeError(
                "result type Float can't be cast to the desired output type Long"
            )
        bool_mask = torch.rand_like(input) > p
        res = bool_mask * input * float(1.0 / (1.0 - p))
        return (res, bool_mask)
    else:
        return (input, torch.ones_like(input, dtype=torch.bool))
