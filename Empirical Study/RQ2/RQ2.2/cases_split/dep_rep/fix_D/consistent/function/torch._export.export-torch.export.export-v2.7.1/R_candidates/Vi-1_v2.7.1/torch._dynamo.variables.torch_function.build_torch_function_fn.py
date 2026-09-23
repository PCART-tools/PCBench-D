def build_torch_function_fn(tx: "InstructionTranslator", value, source):
    from types import FunctionType

    func = value.__torch_function__.__func__

    if not isinstance(func, FunctionType):
        unimplemented("Builtin/C++ torch function implementations NYI")

    source = source and AttrSource(AttrSource(source, "__torch_function__"), "__func__")
    return VariableTracker.build(tx, func, source)
