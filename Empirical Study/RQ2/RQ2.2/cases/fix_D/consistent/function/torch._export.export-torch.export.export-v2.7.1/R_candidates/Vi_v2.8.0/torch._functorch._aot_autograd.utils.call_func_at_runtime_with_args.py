def call_func_at_runtime_with_args(
    f, args: Union[tuple[Any], list[Any]], steal_args=False, disable_amp=False
):
    if not steal_args:
        args = list(args)
    assert isinstance(args, list)

    context = torch._C._DisableAutocast if disable_amp else nullcontext
    with context():
        if getattr(f, "_boxed_call", False):
            out = normalize_as_list(f(args))
        else:
            # TODO: Please remove soon
            # https://github.com/pytorch/pytorch/pull/83137#issuecomment-1211320670
            warnings.warn(
                "Your compiler for AOTAutograd is returning a function that doesn't take boxed arguments. "
                "Please wrap it with functorch.compile.make_boxed_func or handle the boxed arguments yourself. "
                "See https://github.com/pytorch/pytorch/pull/83137#issuecomment-1211320670 for rationale."
            )
            out = normalize_as_list(f(*args))
    return out
