def get_ckpt_filename(node_name, epoch):
    """Returns the checkpoint filename.

    Args:
        node_name: A string. The name of the node.
        epoch: An integer. The checkpoint epoch.

    Returns:
        ckpt_filename: A string. The filename of the checkpoint.
    """
    return node_name + '.' + str(epoch)
