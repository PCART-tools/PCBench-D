def non_single_tensor_return_unsupported(api, ret):
    from . import TensorVariable

    if not isinstance(ret, TensorVariable):
        raise Unsupported(
            f"{api} over function that returns something other than one Tensor"
        )
