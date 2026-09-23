def call_torch_function(
    tx, torch_function_type, torch_function_var, fn, types, args, kwargs
):
    # signature:
    # def __torch_function__(cls, func, types, args=(), kwargs=None):
    tf_args = (
        torch_function_type,
        fn,
        types,
        VariableTracker.build(tx, tuple(args)),
        VariableTracker.build(tx, kwargs),
    )
    return tx.inline_user_function_return(torch_function_var, tf_args, {})
