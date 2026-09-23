def InitOpsLibrary(name, trigger_lazy=True):
    """Loads a dynamic library that contains custom operators into Caffe2.

    Since Caffe2 uses static variable registration, you can optionally load a
    separate .so file that contains custom operators and registers that into
    the caffe2 core binary. In C++, this is usually done by either declaring
    dependency during compilation time, or via dynload. This allows us to do
    registration similarly on the Python side.

    Args:
        name: a name that ends in .so, such as "my_custom_op.so". Otherwise,
            the command will simply be ignored.
    Returns:
        None
    """
    if not os.path.exists(name):
        # Note(jiayq): if the name does not exist, instead of immediately
        # failing we will simply print a warning, deferring failure to the
        # time when an actual call is made.
        print('Ignoring {} as it is not a valid file.'.format(name))
        return
    _init_impl(name, trigger_lazy=trigger_lazy)
