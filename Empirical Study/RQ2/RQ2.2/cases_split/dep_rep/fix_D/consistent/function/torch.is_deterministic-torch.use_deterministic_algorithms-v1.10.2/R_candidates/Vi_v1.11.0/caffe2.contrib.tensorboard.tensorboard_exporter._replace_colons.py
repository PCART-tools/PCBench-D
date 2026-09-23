def _replace_colons(shapes, track_blob_names, ops, repl):
    """
    `:i` has a special meaning in Tensorflow.
    """
    def f(name):
        return name.replace(':', repl)
    _rename_all(shapes, track_blob_names, ops, f)
