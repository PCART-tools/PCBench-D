def _qualified_name(obj) -> str:
    # This special case allows us to override the qualified name on a type.
    # It's currently used in conjunction with tracing, where we create a
    # fake module to filter only supported attributes. However, since this
    # new type is defined as a local class, we need a mechanism to override
    # its qualname so it appears correctly in the TorchScript system. This,
    # we set '_jit_override_qualname' with the original traced module's
    # qualified name, which is picked up here
    if hasattr(obj, '_jit_override_qualname'):
        return obj._jit_override_qualname
    # short-circuit in cases where the object already has a known qualified name
    if isinstance(obj, torch._C.ScriptFunction):
        return obj.qualified_name

    if getattr(obj, "__name__", None):
        name = obj.__name__
    # Enum classes do not have `__name__` attr, instead they have `name`.
    elif isinstance(obj, enum.Enum):
        name = obj.name
    else:
        raise RuntimeError("Could not get name of python class object")


    if name == '<lambda>':
        name = '_lambda'  # make name a valid identifier

    module_name = obj.__module__

    # If the module is actually a torchbind module, then we should short circuit
    if module_name == "torch._classes":
        return obj.qualified_name

    # The Python docs are very clear that `__module__` can be None, but I can't
    # figure out when it actually would be.
    if module_name is None:
        raise RuntimeError(f"Could not get qualified name for class '{name}': "
                           "__module__ can't be None.")

    # if getattr(sys.modules[module_name], name) is not obj:
    #     raise RuntimeError(f"Could not get qualified name for class '{name}': "
    #                        f"the attr {name} on module {module_name} is not the the class")

    # torch.package and TorchScript have separate mangling schemes to avoid
    # name collisions from multiple packages. To avoid them interfering with
    # each other, remove the package mangling here.
    module_name = package_mangling.demangle(module_name)

    # __main__ is a builtin module, so rewrite it to "__torch__".
    if module_name == "__main__":
        module_name = "__torch__"
    else:
        # Everything else gets a "__torch__" prefix to avoid name collisions
        # with the names of user values.
        module_name = "__torch__." + module_name

    if "." in name:
        raise RuntimeError(f"Could not get qualified name for class '{name}': "
                           f"'{name}' is not a valid identifier")

    return module_name + "." + name
