def _drop(fn):
    fn._torchscript_modifier = FunctionModifiers._DROP
    return fn
