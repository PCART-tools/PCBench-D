def _getGradientOrNone(op_proto):
    try:
        grad_ops, _ = gradient_checker.getGradientForOp(op_proto)
        return grad_ops
    except Exception:
        return []
