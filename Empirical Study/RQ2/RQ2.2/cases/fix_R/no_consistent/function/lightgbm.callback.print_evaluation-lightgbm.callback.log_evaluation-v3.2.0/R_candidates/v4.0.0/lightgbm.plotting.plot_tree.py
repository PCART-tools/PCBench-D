def plot_tree(
    booster: Union[Booster, LGBMModel],
    ax=None,
    tree_index: int = 0,
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    show_info: Optional[List[str]] = None,
    precision: Optional[int] = 3,
    orientation: str = 'horizontal',
    example_case: Optional[Union[np.ndarray, pd_DataFrame]] = None,
    **kwargs: Any
) -> Any:
    """Plot specified tree.

    Each node in the graph represents a node in the tree.

    Non-leaf nodes have labels like ``Column_10 <= 875.9``, which means
    "this node splits on the feature named "Column_10", with threshold 875.9".

    Leaf nodes have labels like ``leaf 2: 0.422``, which means "this node is a
    leaf node, and the predicted value for records that fall into this node
    is 0.422". The number (``2``) is an internal unique identifier and doesn't
    have any special meaning.

    .. note::

        It is preferable to use ``create_tree_digraph()`` because of its lossless quality
        and returned objects can be also rendered and displayed directly inside a Jupyter notebook.

    Parameters
    ----------
    booster : Booster or LGBMModel
        Booster or LGBMModel instance to be plotted.
    ax : matplotlib.axes.Axes or None, optional (default=None)
        Target axes instance.
        If None, new figure and axes will be created.
    tree_index : int, optional (default=0)
        The index of a target tree to plot.
    figsize : tuple of 2 elements or None, optional (default=None)
        Figure size.
    dpi : int or None, optional (default=None)
        Resolution of the figure.
    show_info : list of str, or None, optional (default=None)
        What information should be shown in nodes.

            - ``'split_gain'`` : gain from adding this split to the model
            - ``'internal_value'`` : raw predicted value that would be produced by this node if it was a leaf node
            - ``'internal_count'`` : number of records from the training data that fall into this non-leaf node
            - ``'internal_weight'`` : total weight of all nodes that fall into this non-leaf node
            - ``'leaf_count'`` : number of records from the training data that fall into this leaf node
            - ``'leaf_weight'`` : total weight (sum of Hessian) of all observations that fall into this leaf node
            - ``'data_percentage'`` : percentage of training data that fall into this node
    precision : int or None, optional (default=3)
        Used to restrict the display of floating point values to a certain precision.
    orientation : str, optional (default='horizontal')
        Orientation of the tree.
        Can be 'horizontal' or 'vertical'.
    example_case : numpy 2-D array, pandas DataFrame or None, optional (default=None)
        Single row with the same structure as the training data.
        If not None, the plot will highlight the path that sample takes through the tree.

        .. versionadded:: 4.0.0

    **kwargs
        Other parameters passed to ``Digraph`` constructor.
        Check https://graphviz.readthedocs.io/en/stable/api.html#digraph for the full list of supported parameters.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The plot with single tree.
    """
    if MATPLOTLIB_INSTALLED:
        import matplotlib.image as image
        import matplotlib.pyplot as plt
    else:
        raise ImportError('You must install matplotlib and restart your session to plot tree.')

    if ax is None:
        if figsize is not None:
            _check_not_tuple_of_2_elements(figsize, 'figsize')
        _, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    graph = create_tree_digraph(booster=booster, tree_index=tree_index,
                                show_info=show_info, precision=precision,
                                orientation=orientation, example_case=example_case, **kwargs)

    s = BytesIO()
    s.write(graph.pipe(format='png'))
    s.seek(0)
    img = image.imread(s)

    ax.imshow(img)
    ax.axis('off')
    return ax
