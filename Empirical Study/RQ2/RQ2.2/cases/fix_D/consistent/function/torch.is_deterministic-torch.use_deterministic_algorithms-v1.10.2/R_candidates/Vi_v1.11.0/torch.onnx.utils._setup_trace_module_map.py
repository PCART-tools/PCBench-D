def _setup_trace_module_map(model, export_modules_as_functions):
    def __setup_trace_module_map():
        trace_module_map = {_m : torch.typename(type(_m)) for _m in model.modules()}
        torch.jit._trace._trace_module_map = trace_module_map
        return trace_module_map

    if isinstance(export_modules_as_functions, bool) and export_modules_as_functions:
        trace_module_map = __setup_trace_module_map()
        export_modules_as_functions = {v for k, v in trace_module_map.items()}
    elif isinstance(export_modules_as_functions, set) and len(export_modules_as_functions) > 0:
        def _find_typename(v):
            if isinstance(v, type):
                return torch.typename(v)
            else:
                raise RuntimeError("Only type of the `nn.Module` should be "
                                   "passed in the set for argument `export_modules_as_functions`. "
                                   "Got `%s`." % (type(v).__name__))
        trace_module_map = __setup_trace_module_map()
        module_typenames = {_find_typename(v) for v in export_modules_as_functions}
        export_modules_as_functions = module_typenames
    else:
        export_modules_as_functions = None
    return export_modules_as_functions
