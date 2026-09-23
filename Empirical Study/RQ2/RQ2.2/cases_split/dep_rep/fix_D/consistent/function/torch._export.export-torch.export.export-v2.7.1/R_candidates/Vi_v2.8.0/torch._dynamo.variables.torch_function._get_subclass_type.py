def _get_subclass_type(var):
    assert isinstance(var, (TensorWithTFOverrideVariable, UserDefinedObjectVariable))
    return var.python_type()
