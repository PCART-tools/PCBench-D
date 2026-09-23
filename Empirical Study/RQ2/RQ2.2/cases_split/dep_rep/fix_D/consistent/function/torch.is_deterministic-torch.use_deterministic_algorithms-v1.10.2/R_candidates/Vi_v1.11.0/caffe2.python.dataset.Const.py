def Const(net, value, dtype=None, name=None):
    """
    Create a 'constant' by first creating an external input in the given
    net, and then feeding the corresponding blob with its provided value
    in the current workspace. The name is automatically generated in order
    to avoid clashes with existing blob names.
    """
    assert isinstance(net, core.Net), 'net must be a core.Net instance.'
    value = np.array(value, dtype=dtype)
    blob = net.AddExternalInput(net.NextName(prefix=name))
    workspace.FeedBlob(str(blob), value)
    return blob
