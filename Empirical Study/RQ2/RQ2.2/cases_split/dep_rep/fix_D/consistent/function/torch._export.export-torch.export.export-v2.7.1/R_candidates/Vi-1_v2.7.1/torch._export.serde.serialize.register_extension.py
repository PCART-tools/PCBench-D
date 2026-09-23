def register_extension(
    op_type: type[Any],
    extension_handler: type[ExtensionHandler],
):
    """Register custom de/serialization method for a node with non-standard type."""
    assert issubclass(extension_handler, ExtensionHandler), f"Expected ExtensionHandler, got {extension_handler}."
    assert op_type not in _serialization_registry, f"{op_type} is already registered."
    assert isinstance(op_type, type)  # Maybe a good idea to enforce this first.
    assert not (op_type.__module__.startswith("torch") or op_type.__module__.startswith("builtins"))
    assert extension_handler.namespace() not in _deserialization_registry
    _serialization_registry[op_type] = extension_handler
    _deserialization_registry[extension_handler.namespace()] = extension_handler
