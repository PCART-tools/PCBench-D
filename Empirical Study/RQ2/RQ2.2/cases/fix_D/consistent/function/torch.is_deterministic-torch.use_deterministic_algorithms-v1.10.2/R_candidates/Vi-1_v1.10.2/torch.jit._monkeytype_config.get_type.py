def get_type(type):
    """
    Helper function which converts the given type to a torchScript acceptable format.
    """
    if isinstance(type, str):
        return type
    elif inspect.getmodule(type) == typing:
        # If the type is a type imported from typing
        # like Tuple, List, Dict then replace `typing.`
        # with a null string. This needs to be done since
        # typing.List is not accepted by TorchScript.
        type_to_string = str(type)
        return type_to_string.replace(type.__module__ + '.', '')
    elif is_torch_native_class(type):
        # If the type is a subtype of torch module, then TorchScript expects a fully qualified name
        # for the type which is obtained by combining the module name and type name.
        return type.__module__ + '.' + type.__name__
    else:
        # For all other types use the name for the type.
        return type.__name__
