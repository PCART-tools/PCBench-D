def _clear_debug_info(ops, perform_clear):
    '''
    Removes debug information from operators, they are copious.

    Args:
        ops: List of Caffe2 operators
        perform_clear: Boolean passed from _operators_to_graph_def specifying
            whether to remove the debug information. This boolean is passed into
            this function to reduce the complexity of _operators_to_graph_def.

    Returns:
        None. Modifies the list of Caffe2 operators in-place and removes the
        'debug_info' field.

    '''
    if not perform_clear:
        return

    for op in ops:
        if op.HasField('debug_info'):
            op.ClearField('debug_info')
