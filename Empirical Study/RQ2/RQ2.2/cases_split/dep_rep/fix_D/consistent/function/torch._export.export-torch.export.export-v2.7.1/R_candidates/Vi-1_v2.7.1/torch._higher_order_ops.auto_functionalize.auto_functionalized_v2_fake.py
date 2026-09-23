@auto_functionalized_v2.py_impl(FakeTensorMode)
def auto_functionalized_v2_fake(
    mode,
    _mutable_op: OpOverload,
    **kwargs: dict[str, Any],
) -> tuple[Any, tuple[Tensor, ...]]:
    with mode:
        result = auto_functionalized_v2_dense(
            _mutable_op, _only_clone_these_bases=None, **kwargs
        )
        return result
