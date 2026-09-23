def create_script_module(nn_module, stubs_fn, share_types=True, is_tracing=False):
    """
    Creates a new ScriptModule from an nn.Module

    Args:
        nn_module:  The original Python nn.Module that we are creating a ScriptModule for.
        stubs_fn:  Lambda that takes an nn.Module and generates a list of ScriptMethodStubs to compile.
        share_types:  Whether to share underlying JIT types between modules (if possible).
            NOTE: Only set to False this when we cannot guarantee type sharing will work
                correctly. This only happens today for traced modules, where the same
                module can produce different traced methods depending on the inputs.
        is_tracing: Whether this function is called during tracing or scripting. If tracing,
                we don't need to do AttributeTypeIsSupportedChecker because all the unsupported
                attributes will be baked as constant in the tracing graph. In addition,
                this check significantly slows down the traced modules when the module size is big.
    """
    assert not isinstance(nn_module, torch.jit.RecursiveScriptModule)
    check_module_initialized(nn_module)
    concrete_type = get_module_concrete_type(nn_module, share_types)
    if not is_tracing:
        AttributeTypeIsSupportedChecker().check(nn_module)
    return create_script_module_impl(nn_module, concrete_type, stubs_fn)
