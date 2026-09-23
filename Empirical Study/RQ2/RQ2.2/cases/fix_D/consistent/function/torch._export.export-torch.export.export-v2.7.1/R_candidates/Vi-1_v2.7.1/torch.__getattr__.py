    def __getattr__(name):
        # Deprecated attrs
        replacement = _deprecated_attrs.get(name)
        if replacement is not None:
            import warnings

            warnings.warn(
                f"'{name}' is deprecated, please use '{replacement.__module__}.{replacement.__name__}()'",
                stacklevel=2,
            )
            return replacement()

        # Lazy modules
        if name in _lazy_modules:
            return importlib.import_module(f".{name}", __name__)

        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
