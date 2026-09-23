def create_joint(fn: Callable, *, aot_config: AOTConfig) -> Any:
    def inner_fn(primals: list[Any], tangents: list[Any]):
        outs, tangent_mask = fn(*primals)

        assert len(tangent_mask) == len(outs)
        outs_to_grad = [
            o for needs_tangent, o in zip(tangent_mask, outs) if needs_tangent
        ]
        assert len(outs_to_grad) == len(tangents)

        # Get the inputs that need gradients
        grad_primals = []
        inputs_needs_grads = []
        # Note that we're not using primals here,
        # being carefully not to pass any mutated inputs into autograd.grad()
        for p in primals:
            is_grad_tensor = isinstance(p, Tensor) and p.requires_grad
            inputs_needs_grads.append(is_grad_tensor)
            if is_grad_tensor:
                grad_primals.append(p)

        # Get the outputs that need gradients
        needed_outs = []
        needed_tangents = []
        for out, tangent in zip(outs_to_grad, tangents):
            if isinstance(out, Tensor) and out.requires_grad:
                # A bit sketchy, but fixes e.g. test_aot_autograd_exhaustive_matmul_cpu_float32
                # The issue is that we are sensitive to decomps that don't accurately maintain
                # their output's _base.shape compared to eager mode, and this helps mitigate a bit.
                # The guard_or_true also sketchy; if unbacked
                # symints are involved, we're just going to assume that the
                # decomps setup the base shape correctly

                # Return out if the result of out.shape==tangent.shape is unknown or known to be true.
                # otherwise if its a known false return out.view(tangent.shape).
                needed_outs.append(
                    out
                    if guard_or_true(sym_eq(out.shape, tangent.shape))
                    else out.view(tangent.shape)
                )
                needed_tangents.append(tangent)

        setup_stacktrace_preservation_hooks([out.grad_fn for out in needed_outs])

        if config.functionalize_rng_ops:
            PhiloxStateTracker.mark_beginning_of_backward()
        backward_out: tuple[Tensor, ...] = ()
        # Call the backwards pass
        if grad_primals:
            functional_tensor_mode = torch.utils._python_dispatch._detect_infra_mode(
                torch._C._TorchDispatchModeKey.FUNCTIONAL
            )
            if functional_tensor_mode is not None:
                # Side-Effect Tokens:
                # We want to have independent chains of tokens for forward and backward.
                # functional_tensor_mode._tokens is used by both.
                # We memoize the result tokens of forward in functional_tensor_mode._tokens_forward_output,
                # to return them as joint graph outputs.
                # We clean functional_tensor_mode._tokens before backward, to prevent reuse of forward tokens in backward.
                # Joint graph tracing allows tokens discovery,
                # So all the tokens in backward will be created and added as a graph inputs during tracing.
                functional_tensor_mode._tokens_forward_output = (
                    functional_tensor_mode._tokens
                )
                functional_tensor_mode._tokens = {}

            with set_partitioner_tag_is_backward(), fx_traceback.preserve_node_meta():
                # for full graph export, we always export a joint graph where we assume no tangents are needed.
                if aot_config.no_tangents:
                    assert len(needed_tangents) == 1 and needed_tangents[0].numel() == 1
                    backward_out = torch.autograd.grad(
                        needed_outs,
                        grad_primals,
                        allow_unused=True,
                    )
                else:
                    backward_out = torch.autograd.grad(
                        needed_outs,
                        grad_primals,
                        grad_outputs=needed_tangents,
                        allow_unused=True,
                    )
        backward_out_iter = iter(backward_out)
        return outs, [
            next(backward_out_iter) if i else None for i in inputs_needs_grads
        ]

    def inner_fn_with_anomaly(*args):
        with fx_traceback.preserve_node_meta(), warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Anomaly Detection has been enabled.")
            with torch.autograd.detect_anomaly(check_nan=False):
                return inner_fn(*args)

    return inner_fn_with_anomaly
