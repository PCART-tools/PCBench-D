def RegisterLazyImport(lazy):
    global _import_lazy_calls
    _import_lazy_calls += [lazy]
