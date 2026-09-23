def visualize(*args, **kwargs):
    """
    Visualize several dask graphs at once.

    Requires ``graphviz`` to be installed. All options that are not the dask
    graph(s) should be passed as keyword arguments.

    Parameters
    ----------
    dsk : dict(s) or collection(s)
        The dask graph(s) to visualize.
    filename : str or None, optional
        The name (without an extension) of the file to write to disk.  If
        `filename` is None, no file will be written, and we communicate
        with dot using only pipes.
    format : {'png', 'pdf', 'dot', 'svg', 'jpeg', 'jpg'}, optional
        Format in which to write output file.  Default is 'png'.
    optimize_graph : bool, optional
        If True, the graph is optimized before rendering.  Otherwise,
        the graph is displayed as is. Default is False.
    **kwargs
       Additional keyword arguments to forward to ``to_graphviz``.

    Returns
    -------
    result : IPython.diplay.Image, IPython.display.SVG, or None
        See dask.dot.dot_graph for more information.

    See also
    --------
    dask.dot.dot_graph

    Notes
    -----
    For more information on optimization see here:

    http://dask.pydata.org/en/latest/optimize.html
    """

    dsks = [arg for arg in args if isinstance(arg, dict)]
    args = [arg for arg in args if isinstance(arg, Base)]
    filename = kwargs.pop('filename', 'mydask')
    optimize_graph = kwargs.pop('optimize_graph', False)
    from dask.dot import dot_graph
    if optimize_graph:
        dsks.extend([arg._optimize(arg.dask, arg._keys()) for arg in args])
    else:
        dsks.extend([arg.dask for arg in args])
    dsk = merge(dsks)

    return dot_graph(dsk, filename=filename, **kwargs)
