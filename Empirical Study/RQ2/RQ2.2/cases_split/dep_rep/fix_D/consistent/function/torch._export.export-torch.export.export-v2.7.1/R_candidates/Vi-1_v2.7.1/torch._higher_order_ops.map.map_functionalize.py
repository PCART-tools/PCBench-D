@map_impl.py_functionalize_impl
def map_functionalize(ctx, f, xs, pos_args):
    unwrapped_xs = ctx.unwrap_tensors(xs)
    unwrapped_args = ctx.unwrap_tensors(pos_args)
    wrapped_fn = ctx.functionalize(_maybe_run_with_interpreter(f))

    with ctx.redispatch_to_next():
        with disable_proxy_modes_tracing():
            example_inputs = (*_unstack_pytree(unwrapped_xs)[0], *unwrapped_args)
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        if _has_potential_branch_input_mutation(
            f, example_inputs, pre_dispatch=pre_dispatch
        ):
            raise UnsupportedAliasMutationException("torch.map is mutating the input!")

        if _has_potential_branch_input_alias(
            f, example_inputs, pre_dispatch=pre_dispatch
        ):
            raise UnsupportedAliasMutationException("torch.map is aliasing the input!")

        map_return = map_impl(wrapped_fn, unwrapped_xs, unwrapped_args)
        return ctx.wrap_tensors(map_return)
