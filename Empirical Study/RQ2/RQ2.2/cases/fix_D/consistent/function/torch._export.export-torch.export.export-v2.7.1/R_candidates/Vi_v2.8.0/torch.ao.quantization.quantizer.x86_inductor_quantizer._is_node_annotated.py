def _is_node_annotated(_node):
    """
    return True if the node is annotated, otherwise return False
    """
    return (
        QUANT_ANNOTATION_KEY in _node.meta
        and _node.meta[QUANT_ANNOTATION_KEY]._annotated
    )
