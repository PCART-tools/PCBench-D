def StartMint(root_folder=None, port=None):
    """Start a mint instance.

    TODO(Yangqing): this does not work well under ipython yet. According to
        https://github.com/ipython/ipython/issues/5862
    writing up some fix is a todo item.
    """
    from caffe2.python.mint import app
    if root_folder is None:
        # Get the root folder from the current workspace
        root_folder = C.root_folder()
    if port is None:
        port = _GetFreeFlaskPort()
    process = Process(
        target=app.main,
        args=(
            ['-p', str(port), '-r', root_folder],
        )
    )
    process.start()
    print('Mint running at http://{}:{}'.format(socket.getfqdn(), port))
    return process
