def wrap_args_kwargs(tx: "InstructionTranslator", result):
    for k, v in list(result.items()):
        if isinstance(v, (tuple, dict)):
            # args/kwargs
            result[k] = wrap_bound_arg(tx, v)
