@contextlib.contextmanager
def disable_apex_o2_state_dict_hook(model):
    # Apex O2 hook state_dict to return fp16 weights as fp32.
    # Exporter cannot identify them as same tensors.
    # Since this hook is only used by optimizer, it is safe to
    # remove this hook while exporting.
    if not isinstance(model, torch.jit.ScriptFunction):
        tmp_map = {}  # type: ignore[var-annotated]
        for module in model.modules():
            for k, v in module._state_dict_hooks.items():
                if type(v).__name__ == 'O2StateDictHook':
                    if module not in tmp_map:
                        tmp_map[module] = {}
                    tmp_map[module][k] = v
            if module in tmp_map:
                for k in tmp_map[module].keys():
                    module._state_dict_hooks.pop(k)
    try:
        yield
    finally:
        if not isinstance(model, torch.jit.ScriptFunction):
            for module, m_map in tmp_map.items():
                for k, v in m_map.items():
                    module._state_dict_hooks[k] = v
