def register_op_impl(run_impl_check: Union[Callable[[OpOverload], bool], OpOverload]):
    def impl_decorator(op_impl):
        if isinstance(run_impl_check, OpOverload):
            assert (
                run_impl_check not in op_implementations_dict
            ), f"duplicate registration: {run_impl_check}"
            op_implementations_dict[run_impl_check] = op_impl
        elif isinstance(run_impl_check, (list, tuple)):
            for op in run_impl_check:
                register_op_impl(op)(op_impl)
        else:
            assert callable(run_impl_check)
            op_implementations_checks.append((run_impl_check, op_impl))

        return op_impl

    return impl_decorator
