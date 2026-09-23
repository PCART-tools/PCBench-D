def IsOperatorWithEngine(op_type, engine):
    TriggerLazyImport()
    return C.op_registry_key(op_type, engine) in _REGISTERED_OPERATORS
