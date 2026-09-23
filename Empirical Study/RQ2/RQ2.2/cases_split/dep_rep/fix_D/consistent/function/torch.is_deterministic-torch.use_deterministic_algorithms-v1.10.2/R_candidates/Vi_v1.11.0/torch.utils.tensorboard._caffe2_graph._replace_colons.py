def _replace_colons(shapes, blob_name_tracker, ops, repl):
    '''
    `:i` has a special meaning in Tensorflow. This function replaces all colons
    with $ to avoid any possible conflicts.

    Args:
        shapes: Dictionary mapping blob names to their shapes/dimensions.
        blob_name_tracker: Dictionary of all unique blob names (with respect to
            some context).
        ops: List of Caffe2 operators
        repl: String representing the text to replace ':' with. Usually this is
            '$'.

    Returns:
        None. Modifies blob_name_tracker in-place.

    '''
    def f(name):
        return name.replace(':', repl)
    _rename_all(shapes, blob_name_tracker, ops, f)
