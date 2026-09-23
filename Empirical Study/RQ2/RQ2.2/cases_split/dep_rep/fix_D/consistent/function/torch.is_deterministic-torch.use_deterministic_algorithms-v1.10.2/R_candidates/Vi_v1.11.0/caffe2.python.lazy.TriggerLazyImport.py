def TriggerLazyImport():
    global _import_lazy_calls
    for lazy in _import_lazy_calls:
        lazy()
