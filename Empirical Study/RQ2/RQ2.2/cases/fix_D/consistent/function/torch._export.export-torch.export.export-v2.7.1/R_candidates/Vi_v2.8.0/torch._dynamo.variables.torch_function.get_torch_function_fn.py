def get_torch_function_fn(tx: "InstructionTranslator", vt):
    # The underlying function could be a classmethod, staticmethod, regular
    # function or a function with C-implementation. It doesn't matter as long as
    # they satisfy the calling convention in `call_torch_function`.
    from .builtin import BuiltinVariable

    args = [vt, ConstantVariable("__torch_function__")]
    func_vt = BuiltinVariable(getattr).call_function(tx, args, {})
    return func_vt
