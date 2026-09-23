def _cdiv(
    x: Union[int, float, torch.Tensor], multiple: Union[int, float, torch.Tensor]
):
    return (x + multiple - 1) // multiple
