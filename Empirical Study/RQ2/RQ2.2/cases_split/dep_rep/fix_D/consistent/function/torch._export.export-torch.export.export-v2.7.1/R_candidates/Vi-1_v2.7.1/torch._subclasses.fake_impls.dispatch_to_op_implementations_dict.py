@register_op_impl(op_implementations_dict.__contains__)
def dispatch_to_op_implementations_dict(fake_mode, func, *args, **kwargs):
    return op_implementations_dict[func](fake_mode, func, *args, **kwargs)
