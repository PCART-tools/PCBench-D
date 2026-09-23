def _deregister_op_impl(op):
    if op in op_implementations_dict:
        del op_implementations_dict[op]
    for check, impl in op_implementations_checks:
        if check is op:
            op_implementations_checks.remove((check, impl))
            break
