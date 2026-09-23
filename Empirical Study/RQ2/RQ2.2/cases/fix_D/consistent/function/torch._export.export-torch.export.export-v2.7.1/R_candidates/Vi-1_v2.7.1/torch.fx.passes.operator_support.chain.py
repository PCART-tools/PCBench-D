@compatibility(is_backward_compatible=False)
def chain(*op_support: OperatorSupportBase) -> OperatorSupportBase:
    """Combines a sequence of `OperatorSupportBase` instances to form a single `OperatorSupportBase`
    instance by evaluating each input `OperatorSupportBase` instance, and returns False if
    any of it reports False.
    """

    def _chain(submods, node) -> bool:
        return all(x.is_node_supported(submods, node) for x in op_support)

    return create_op_support(_chain)
