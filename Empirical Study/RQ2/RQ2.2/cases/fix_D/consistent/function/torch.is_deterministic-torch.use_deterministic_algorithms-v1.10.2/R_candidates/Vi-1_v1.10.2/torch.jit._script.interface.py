def interface(obj):
    if not inspect.isclass(obj):
        raise RuntimeError("interface must be applied to a class")
    if not _is_new_style_class(obj):
        raise RuntimeError("TorchScript interfaces must inherit from 'object'")

    # Expected MRO is:
    #   User module
    #   torch.nn.modules.module.Module
    #   object
    is_module_interface = issubclass(obj, torch.nn.Module) and len(obj.mro()) == 3

    if not is_module_interface and len(obj.mro()) > 2:
        raise RuntimeError(
            "TorchScript interface does not support inheritance yet. "
            "Please directly inherit from 'object' or 'nn.Module'."
        )

    qualified_name = _qualified_name(obj)
    rcb = _jit_internal.createResolutionCallbackFromFrame(1)
    # if this type is a `nn.Module` subclass, generate a module interface type
    # instead of a class interface type; a module interface type only compiles
    # the user provided methods as part of the interface
    ast = get_jit_class_def(obj, obj.__name__)
    mangled_classname = torch._C._jit_script_interface_compile(
        qualified_name, ast, rcb, is_module_interface
    )
    obj.__torch_script_interface__ = mangled_classname
    return obj
