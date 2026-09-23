@set_module('numpy')
def info(object=None, maxwidth=76, output=None, toplevel='numpy'):
    """
    Get help information for a function, class, or module.

    Parameters
    ----------
    object : object or str, optional
        Input object or name to get information about. If `object` is a
        numpy object, its docstring is given. If it is a string, available
        modules are searched for matching objects.  If None, information
        about `info` itself is returned.
    maxwidth : int, optional
        Printing width.
    output : file like object, optional
        File like object that the output is written to, default is
        ``None``, in which case ``sys.stdout`` will be used.
        The object has to be opened in 'w' or 'a' mode.
    toplevel : str, optional
        Start search at this level.

    See Also
    --------
    source, lookfor

    Notes
    -----
    When used interactively with an object, ``np.info(obj)`` is equivalent
    to ``help(obj)`` on the Python prompt or ``obj?`` on the IPython
    prompt.

    Examples
    --------
    >>> np.info(np.polyval) # doctest: +SKIP
       polyval(p, x)
         Evaluate the polynomial p at x.
         ...

    When using a string for `object` it is possible to get multiple results.

    >>> np.info('fft') # doctest: +SKIP
         *** Found in numpy ***
    Core FFT routines
    ...
         *** Found in numpy.fft ***
     fft(a, n=None, axis=-1)
    ...
         *** Repeat reference found in numpy.fft.fftpack ***
         *** Total of 3 references found. ***

    """
    global _namedict, _dictlist
    # Local import to speed up numpy's import time.
    import pydoc
    import inspect

    if (hasattr(object, '_ppimport_importer') or
           hasattr(object, '_ppimport_module')):
        object = object._ppimport_module
    elif hasattr(object, '_ppimport_attr'):
        object = object._ppimport_attr

    if output is None:
        output = sys.stdout

    if object is None:
        info(info)
    elif isinstance(object, ndarray):
        _info(object, output=output)
    elif isinstance(object, str):
        if _namedict is None:
            _namedict, _dictlist = _makenamedict(toplevel)
        numfound = 0
        objlist = []
        for namestr in _dictlist:
            try:
                obj = _namedict[namestr][object]
                if id(obj) in objlist:
                    print("\n     "
                          "*** Repeat reference found in %s *** " % namestr,
                          file=output
                          )
                else:
                    objlist.append(id(obj))
                    print("     *** Found in %s ***" % namestr, file=output)
                    info(obj)
                    print("-"*maxwidth, file=output)
                numfound += 1
            except KeyError:
                pass
        if numfound == 0:
            print("Help for %s not found." % object, file=output)
        else:
            print("\n     "
                  "*** Total of %d references found. ***" % numfound,
                  file=output
                  )

    elif inspect.isfunction(object) or inspect.ismethod(object):
        name = object.__name__
        try:
            arguments = str(inspect.signature(object))
        except Exception:
            arguments = "()"

        if len(name+arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments

        print(" " + argstr + "\n", file=output)
        print(inspect.getdoc(object), file=output)

    elif inspect.isclass(object):
        name = object.__name__
        try:
            arguments = str(inspect.signature(object))
        except Exception:
            arguments = "()"

        if len(name+arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments

        print(" " + argstr + "\n", file=output)
        doc1 = inspect.getdoc(object)
        if doc1 is None:
            if hasattr(object, '__init__'):
                print(inspect.getdoc(object.__init__), file=output)
        else:
            print(inspect.getdoc(object), file=output)

        methods = pydoc.allmethods(object)

        public_methods = [meth for meth in methods if meth[0] != '_']
        if public_methods:
            print("\n\nMethods:\n", file=output)
            for meth in public_methods:
                thisobj = getattr(object, meth, None)
                if thisobj is not None:
                    methstr, other = pydoc.splitdoc(
                            inspect.getdoc(thisobj) or "None"
                            )
                print("  %s  --  %s" % (meth, methstr), file=output)

    elif hasattr(object, '__doc__'):
        print(inspect.getdoc(object), file=output)
