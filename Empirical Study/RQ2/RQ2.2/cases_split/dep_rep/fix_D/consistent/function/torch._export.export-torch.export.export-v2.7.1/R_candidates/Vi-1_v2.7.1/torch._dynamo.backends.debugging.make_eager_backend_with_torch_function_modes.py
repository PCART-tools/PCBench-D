def make_eager_backend_with_torch_function_modes(modes):
    """Used to trace HOPs (cond and while) for eager exectution, the metadata
    TF mode mutates vars outside of the scope of the HOP, and we can't have graph breaks
    in the HOP, so we need to externally run this mode and not trace it."""
    from contextlib import ExitStack

    def fn(gm, fake_tensor_inputs, **kwargs):
        stack = ExitStack()
        for mode in modes:
            stack.enter_context(mode)

        result = gm.forward
        stack.close()
        return result

    return fn
