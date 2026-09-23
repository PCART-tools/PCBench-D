@functools.lru_cache(None)
def get_overridable_functions() -> Dict[Any, List[Callable]]:
    """List functions that are overridable via __torch_function__

    Returns
    -------
    Dict[Any, List[Callable]]
        A dictionary that maps namespaces that contain overridable functions
        to functions in that namespace that can be overridden.
    """
    overridable_funcs = collections.defaultdict(list)
    tested_namespaces = [
        (torch, torch.__all__ + dir(torch._C._VariableFunctions)),
        (torch.functional, torch.functional.__all__),
        (torch.nn.functional, dir(torch.nn.functional)),
        (torch.Tensor, dir(torch.Tensor)),
        (torch.linalg, dir(torch.linalg)),
        (torch.fft, dir(torch.fft)),
        (torch.special, dir(torch.special)),
    ]
    for namespace, ns_funcs in tested_namespaces:
        for func_name in ns_funcs:
            # ignore private functions or functions that are deleted in torch.__init__
            if namespace is not torch.Tensor:
                if func_name.startswith('_'):
                    continue
                elif func_name.endswith('_'):
                    continue
                elif not func_name[0].islower():
                    continue
                elif func_name == 'unique_dim':
                    continue
            else:
                func = getattr(namespace, func_name)
                if getattr(object, func_name, None) == func:
                    continue
                if func_name == '__weakref__':
                    continue
            func = getattr(namespace, func_name)
            if namespace is torch.Tensor and getattr(object, func_name, None) == func:
                continue
            # ignore re-exported modules
            if isinstance(func, types.ModuleType):
                continue
            # ignore __future__ imports
            if isinstance(func, __future__._Feature):
                continue

            if not callable(func) and hasattr(func, "__get__"):
                if func.__get__ in get_ignored_functions():
                    msg = ("{}.{} is in the tuple returned by torch._overrides.get_ignored_functions "
                           "but still has an explicit override")
                    assert func.__get__ not in get_testing_overrides(), msg.format(namespace, func.__name__)
                    continue
                else:
                    overridable_funcs[func].append(func.__get__)
                    continue

            if not callable(func):
                continue

            # cannot be overriden by __torch_function__
            if func in get_ignored_functions():
                msg = ("{}.{} is in the tuple returned by torch._overrides.get_ignored_functions "
                       "but still has an explicit override")
                assert func not in get_testing_overrides(), msg.format(namespace, func.__name__)
                continue
            overridable_funcs[namespace].append(func)
    return overridable_funcs
