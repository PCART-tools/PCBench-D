def handle_effect_tokens_fn(
    fn,
    args,
    *,
    meta: ViewAndMutationMeta,
    trace_joint: bool,
) -> Any:
    num_tokens = len(meta.tokens)

    @wraps(fn)
    def inner_fn(*args):
        # See Note [Disabling Functionalize TLS Above Python Functionalization]
        disable_above = torch._C._ExcludeDispatchKeyGuard(
            torch._C.DispatchKeySet(torch._C.DispatchKey.Functionalize)
        )

        with disable_above:
            # See Note [Side-Effectful Tokens in AOTAutograd]
            if trace_joint:
                assert isinstance(args, tuple) and isinstance(args[0], (list, tuple))
                tokens = args[0][:num_tokens]
                assert all(token.numel() == 0 for token in tokens)
                args = (args[0][num_tokens:], *args[1:])
            else:
                tokens = args[:num_tokens]
                assert all(token.numel() == 0 for token in tokens)
                args = args[num_tokens:]

            # Populate the current FunctionalTensorMode with the tokens per
            # operator. See Note [FunctionalTensorMode is Stateful]
            functional_tensor_mode = torch.utils._python_dispatch._detect_infra_mode(
                torch._C._TorchDispatchModeKey.FUNCTIONAL
            )
            assert functional_tensor_mode is not None
            f_tokens = pytree.tree_map(to_fun, tokens)
            for i, k in enumerate(meta.tokens.keys()):
                functional_tensor_mode._tokens[k] = f_tokens[i]

            # Run the joint
            outs = fn(*args)

        # Return both the tokens and the outputs
        # See Note [Side-Effectful Tokens in AOTAutograd]
        if trace_joint:
            assert len(outs) == 2
            assert len(functional_tensor_mode._tokens_forward_output) == num_tokens
            fwd_out_tokens = functional_tensor_mode._tokens_forward_output.values()

            bwd_out_tokens = functional_tensor_mode._tokens.values()

            f_fwd_out_tokens = [from_fun(t) for t in fwd_out_tokens]
            f_bwd_out_tokens = [from_fun(t) for t in bwd_out_tokens]

            meta.num_backward_tokens = len(bwd_out_tokens)
            return ((*f_fwd_out_tokens, *outs[0]), (*outs[1], *f_bwd_out_tokens))

        out_tokens = [from_fun(t) for t in functional_tensor_mode._tokens.values()]
        return (*out_tokens, *outs)

    # Additionally pass in tokens as inputs
    # See Note [Side-Effectful Tokens in AOTAutograd]
    additional_fwd_token_inputs = [torch.tensor([])] * num_tokens

    if trace_joint:
        args = ([*additional_fwd_token_inputs, *args[0]], *args[1:])
    else:
        args = [*additional_fwd_token_inputs, *args]
    return inner_fn, args
