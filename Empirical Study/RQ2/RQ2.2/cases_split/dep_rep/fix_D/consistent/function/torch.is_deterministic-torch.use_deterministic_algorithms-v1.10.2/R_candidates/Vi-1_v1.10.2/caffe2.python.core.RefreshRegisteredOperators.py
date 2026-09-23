def RefreshRegisteredOperators(trigger_lazy=True):
    if trigger_lazy:
        TriggerLazyImport()
    global _REGISTERED_OPERATORS
    _REGISTERED_OPERATORS = _GetRegisteredOperators()
