def _check_composite_compliance(op, args, kwargs):
    def wrap(e):
        return CompositeCompliantTensor(e) if isinstance(e, torch.Tensor) else e

    args = tree_map(wrap, args)
    kwargs = tree_map(wrap, kwargs)
    try:
        with enable_python_mode(CompositeCompliantTensor):
            op(*args, **kwargs)
    except RuntimeError as err:
        raise RuntimeError("CompositeImplicitAutograd compilance check failed with "
                           "the above error. If you are adding an OpInfo of an "
                           "existing operator, please feel free to skip this test "
                           "because the problem was pre-existing and file an issue. "
                           "Otherwise, if you added a new operator, please read "
                           "through the CompositeImplicitAutograd Compliance section in "
                           "aten/src/ATen/native/README.md for how to resolve this. "
                           ) from err
