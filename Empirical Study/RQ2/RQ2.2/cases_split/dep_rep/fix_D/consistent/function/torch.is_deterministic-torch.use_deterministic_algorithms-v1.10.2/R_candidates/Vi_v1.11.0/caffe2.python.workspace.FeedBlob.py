def FeedBlob(name, arr, device_option=None):
    """Feeds a blob into the workspace.

    Inputs:
      name: the name of the blob.
      arr: either a TensorProto object or a numpy array object to be fed into
          the workspace.
      device_option (optional): the device option to feed the data with.
    Returns:
      True or False, stating whether the feed is successful.
    """
    ws = C.Workspace.current
    return _Workspace_feed_blob(ws, name, arr, device_option)
