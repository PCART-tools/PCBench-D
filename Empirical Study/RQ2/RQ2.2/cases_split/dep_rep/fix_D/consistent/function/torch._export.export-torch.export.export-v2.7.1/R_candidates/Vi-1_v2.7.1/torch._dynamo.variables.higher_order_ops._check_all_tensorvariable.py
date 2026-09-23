def _check_all_tensorvariable(args):
    from . import TensorVariable

    if not all(type(a.realize()) is TensorVariable for a in args):
        unimplemented(
            f"Expected all leaves to be of torch.Tensor type, but got {[type(a.realize()) for a in args]}."
        )
