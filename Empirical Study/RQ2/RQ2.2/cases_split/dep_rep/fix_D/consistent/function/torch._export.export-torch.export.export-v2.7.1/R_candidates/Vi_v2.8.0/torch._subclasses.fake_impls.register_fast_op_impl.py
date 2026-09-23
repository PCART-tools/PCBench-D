def register_fast_op_impl(func: OpOverload):
    def impl_decorator(op_impl):
        FAST_OP_IMPLEMENTATIONS[func] = op_impl
        return op_impl

    return impl_decorator
