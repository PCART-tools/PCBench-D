def open_file(path_arg, mode="r"):
    """Decorator to ensure clean opening and closing of files.

    Parameters
    ----------
    path_arg : string or int
        Name or index of the argument that is a path.

    mode : str
        String for opening mode.

    Returns
    -------
    _open_file : function
        Function which cleanly executes the io.

    Examples
    --------
    Decorate functions like this::

       @open_file(0,"r")
       def read_function(pathname):
           pass

       @open_file(1,"w")
       def write_function(G, pathname):
           pass

       @open_file(1,"w")
       def write_function(G, pathname="graph.dot"):
           pass

       @open_file("pathname","w")
       def write_function(G, pathname="graph.dot"):
           pass

       @open_file("path", "w+")
       def another_function(arg, **kwargs):
           path = kwargs["path"]
           pass

    Notes
    -----
    Note that this decorator solves the problem when a path argument is
    specified as a string, but it does not handle the situation when the
    function wants to accept a default of None (and then handle it).

    Here is an example of how to handle this case::

      @open_file("path")
      def some_function(arg1, arg2, path=None):
         if path is None:
             fobj = tempfile.NamedTemporaryFile(delete=False)
         else:
             # `path` could have been a string or file object or something
             # similar. In any event, the decorator has given us a file object
             # and it will close it for us, if it should.
             fobj = path

         try:
             fobj.write("blah")
         finally:
             if path is None:
                 fobj.close()

    Normally, we'd want to use "with" to ensure that fobj gets closed.
    However, the decorator will make `path` a file object for us,
    and using "with" would undesirably close that file object.
    Instead, we use a try block, as shown above.
    When we exit the function, fobj will be closed, if it should be, by the decorator.
    """

    def _open_file(path):
        # Now we have the path_arg. There are two types of input to consider:
        #   1) string representing a path that should be opened
        #   2) an already opened file object
        if isinstance(path, str):
            ext = splitext(path)[1]
        elif isinstance(path, Path):
            # path is a pathlib reference to a filename
            ext = path.suffix
            path = str(path)
        else:
            # could be None, or a file handle, in which case the algorithm will deal with it
            return path, lambda: None

        fobj = _dispatch_dict[ext](path, mode=mode)
        return fobj, lambda: fobj.close()

    return argmap(_open_file, path_arg, try_finally=True)
