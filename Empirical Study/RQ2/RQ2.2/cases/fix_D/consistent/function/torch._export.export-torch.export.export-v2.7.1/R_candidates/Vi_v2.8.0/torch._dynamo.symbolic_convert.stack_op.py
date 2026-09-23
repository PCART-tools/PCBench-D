def stack_op(fn: typing.Callable[..., object]):
    nargs = len(inspect.signature(fn).parameters)
    fn_var = BuiltinVariable(fn)

    @functools.wraps(fn)
    def impl(self: "InstructionTranslator", inst: Instruction):
        self.push(fn_var.call_function(self, self.popn(nargs), {}))

    return impl
