def safe_fake_check(
    op: torch._ops.OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    copy_inputs: bool = True,
    rtol: Optional[float] = None,
    atol: Optional[float] = None,
) -> None:
    if pytree.tree_any_only(torch.Tensor, is_abstract, (args, kwargs)):
        return None
    if copy_inputs:
        args, kwargs = deepcopy_tensors((args, kwargs))
    return fake_check(op, args, kwargs)
