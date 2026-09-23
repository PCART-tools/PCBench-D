@while_loop_op.py_impl(DispatchKey.CompositeExplicitAutograd)
def while_loop_dense(cond_fn, body_fn, carried_inputs, additional_inputs):
    carried_vals = carried_inputs

    def _validate_cond_output(pred):
        if (
            isinstance(pred, torch.Tensor)
            and pred.size() == torch.Size([])
            and pred.dtype == torch.bool
        ) or isinstance(pred, bool):
            return
        else:
            raise RuntimeError(
                f"cond_fn must return a boolean scalar tensor or a boolean but got {pred}"
            )

    if not isinstance(carried_inputs, (tuple, list)):
        raise RuntimeError(
            f"carried_inputs must be a tuple or list but got {type(carried_inputs)}"
        )

    while pred := cond_fn(*carried_vals, *additional_inputs):
        _validate_cond_output(pred)
        out = body_fn(*carried_vals, *additional_inputs)
        assert isinstance(
            out, tuple
        ), f"body_fn should return a tuple but got {type(out)}"
        assert len(out) == len(
            carried_inputs
        ), "body_fn should return the same number of elements as carried_inputs"
        carried_vals = out
    return carried_vals
