def _wrap_all_tensors_to_functional(
    tensor_pytree, level, *, _python_functionalize: bool = False
):
    return tree_map(
        partial(
            lambda x: _maybe_wrap_functional_tensor(
                x, level, _python_functionalize=_python_functionalize
            )
        ),
        tensor_pytree,
    )
