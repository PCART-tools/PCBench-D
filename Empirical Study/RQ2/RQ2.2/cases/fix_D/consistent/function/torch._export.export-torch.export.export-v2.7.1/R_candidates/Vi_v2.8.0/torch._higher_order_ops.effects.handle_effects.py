def handle_effects(
    allow_token_discovery: bool,
    tokens: dict[_EffectType, torch.Tensor],
    op: OpType,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    """
    Args:
        allow_token_discovery: Whether or not we are discovering tokens. If this
        is true, we will create a token for every side effect type seen that
        does not have a token assigned yet.  If this is false, the tokens
        should've all been created ahead of time, so we will error if there is
        no token mapping to every effect type.

        tokens: Map of effect type to tokens. This is to chain operators of the
        same effects together so that they do not get reordered in later
        optimization passes.
    """

    # Get a token. We can't do `tokens.get(op, torch.tensor([]))` because
    # this will create an empty tensor during proxy mode tracing if the token
    # doesn't exist. But the tokens should always exist during proxy mode tracing.
    key = get_effect_key(op, args, kwargs)
    assert key is not None
    if key not in tokens:
        assert (
            allow_token_discovery
        ), f"Could not find a token for effect {key} which came from the function {op}"
        proxy_tensor_mode = torch._C._get_dispatch_mode(
            torch._C._TorchDispatchModeKey.PROXY
        )
        if proxy_tensor_mode is not None:
            # If we discovered a new token during tracing, we are in backward.
            # Then we patch the graph, adding additional tangents_token as input to the joint graph.
            tracer = proxy_tensor_mode.tracer

            from torch.fx.experimental.proxy_tensor import (
                disable_proxy_modes_tracing,
                track_tensor_tree,
            )

            with disable_proxy_modes_tracing():
                token_tensor = new_token_tensor()

            token_proxy = proxy_tensor_mode.tracer.create_proxy(
                "placeholder", "tangents_token", (), {}, name="tangents_token"
            )
            track_tensor_tree(token_tensor, token_proxy, constant=None, tracer=tracer)

            tokens[key] = token_tensor
        else:
            tokens[key] = new_token_tensor()

    token = tokens[key]

    from torch._subclasses.functional_tensor import PythonFunctionalizeAPI

    ctx = PythonFunctionalizeAPI()

    unwrapped_token = ctx.unwrap_tensors([token])[0]
    unwrapped_args = ctx.unwrap_tensors(args)
    unwrapped_kwargs = ctx.unwrap_tensors(kwargs)  # type: ignore[arg-type]
    with ctx.redispatch_to_next():
        (new_token, *unwrapped_outs) = with_effects(
            unwrapped_token, op, *unwrapped_args, **unwrapped_kwargs
        )

    schema = _get_schema(op, unwrapped_args)
    if len(schema.returns) == 0:
        assert unwrapped_outs[0] is None
        unwrapped_outs = None  # type: ignore[assignment]
    elif len(schema.returns) == 1:
        assert len(unwrapped_outs) == 1
        unwrapped_outs = unwrapped_outs[0]
    else:
        assert len(unwrapped_outs) == len(schema.returns)

    # Add the newly created token into the tokens map for a following call to
    # use this token.
    wrapped_token = ctx.wrap_tensors(new_token)
    assert isinstance(wrapped_token, torch.Tensor)
    tokens[key] = wrapped_token

    return ctx.wrap_tensors(unwrapped_outs)
