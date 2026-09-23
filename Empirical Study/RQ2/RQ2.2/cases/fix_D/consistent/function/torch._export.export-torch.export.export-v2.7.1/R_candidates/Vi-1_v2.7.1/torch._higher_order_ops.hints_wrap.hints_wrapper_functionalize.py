@hints_wrapper.py_functionalize_impl
def hints_wrapper_functionalize(ctx, body_fn, args, kwargs, hints):
    unwrapped_args = ctx.unwrap_tensors(args)
    unwrapped_kwargs = ctx.unwrap_tensors(kwargs)
    unwrapped_hints = ctx.unwrap_tensors(hints)
    with ctx.redispatch_to_next():
        functional_body_fn = ctx.functionalize(body_fn)
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        if _has_potential_branch_input_mutation(
            body_fn, unwrapped_args, pre_dispatch=pre_dispatch
        ):
            raise UnsupportedAliasMutationException(
                "body_fn of hints_wrapper might be modifying the input!"
            )
        if _has_potential_branch_input_alias(
            body_fn, unwrapped_args, pre_dispatch=pre_dispatch
        ):
            raise UnsupportedAliasMutationException(
                "body_fn of hints_wrapper might be aliasing the input!"
            )
        outputs = hints_wrapper(
            functional_body_fn,
            unwrapped_args,
            unwrapped_kwargs,
            unwrapped_hints,
        )
        return ctx.wrap_tensors(outputs)
