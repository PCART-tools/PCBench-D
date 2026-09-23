def register_acc_op_properties(*properties: AccOpProperty):
    """
    Attach properties to acc_op to inform optimization
    """
    def decorator(acc_op: Callable):
        acc_op_properties[acc_op] |= set(properties)
        for prop in properties:
            acc_ops_with_property[prop].add(acc_op)
        return acc_op
    return decorator
