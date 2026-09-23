def is_hashable(x):
    # NB - performing isinstance check on a LazVT realizes the VT, accidentally
    # inserting the guard. To avoid this, lazyVT `is_hashable` methods looks at
    # the underlying value without realizing the VT. Consider updating the
    # lazyVT `is_hashable` method if you see unnecessary guarding for a key VT.
    if (
        isinstance(x, variables.LazyVariableTracker)
        and not x.is_realized()
        and x.is_hashable()
    ):
        return True

    if isinstance(x, variables.TensorVariable):
        # Tensors are hashable if they have an example_value (a fake tensor)
        # Most VT's should have one.
        # It'd be nice if at some point we could assert that they all have one
        return x.as_proxy().node.meta.get("example_value") is not None
    elif isinstance(x, variables.TupleVariable):
        return all(is_hashable(e) for e in x.items)
    else:
        return isinstance(
            x,
            (
                variables.BuiltinVariable,
                variables.SymNodeVariable,
                variables.ConstantVariable,
                variables.EnumVariable,
                variables.user_defined.UserDefinedClassVariable,
                variables.UserFunctionVariable,
                variables.SkipFunctionVariable,
                variables.misc.NumpyVariable,
                variables.NNModuleVariable,
                variables.UnspecializedNNModuleVariable,
                variables.MethodWrapperVariable,
                variables.TorchInGraphFunctionVariable,
                variables.TypingVariable,
                variables.FunctoolsPartialVariable,
                variables.WeakRefVariable,
            ),
        )
