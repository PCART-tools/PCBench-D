def call_prepare_scriptable_func(obj):
    memo: Dict[int, torch.nn.Module] = {}
    return call_prepare_scriptable_func_impl(obj, memo)
