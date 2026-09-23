def _get_subclass_type_var(tx: "InstructionTranslator", var):
    assert isinstance(var, (TensorWithTFOverrideVariable, UserDefinedObjectVariable))
    if isinstance(var, TensorWithTFOverrideVariable):
        return var.class_type_var(tx)
    elif isinstance(var, UserDefinedObjectVariable):
        source = var.source and TypeSource(var.source)
        return VariableTracker.build(tx, var.python_type(), source)
