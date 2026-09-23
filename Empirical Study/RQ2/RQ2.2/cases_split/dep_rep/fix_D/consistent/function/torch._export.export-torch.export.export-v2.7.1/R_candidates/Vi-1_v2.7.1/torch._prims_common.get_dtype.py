def get_dtype(x: Union[torch.Tensor, NumberType]):
    if isinstance(x, torch.Tensor):
        return x.dtype
    else:
        return type_to_dtype(type(x))
