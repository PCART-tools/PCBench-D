def db_name(epoch, node_name, db_prefix, path_prefix=None):
    """Returns the full db name where checkpoint files are saved.

    Args:
        epoch: An integer. The checkpoint epoch.
        node_name: A string. The name of the node.
        db_prefix: A string. The prefix used to construct full db name.
        path_prefix: A string. Optional param used to construct db name or path
            where checkpoint files are are stored.
    Returns:
        db_name: A string. The absolute path of full_db_name where checkpoint
            files are saved
    """
    if path_prefix:
        db_name = path_prefix + get_ckpt_filename(node_name, epoch)
    else:
        ckpt_filename = get_ckpt_filename(node_name, epoch)
        db_name = os.path.join(db_prefix, ckpt_filename)
    return db_name
