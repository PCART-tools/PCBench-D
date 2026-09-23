def create_tree_digraph(
    booster: Union[Booster, LGBMModel],
    tree_index: int = 0,
    show_info: Optional[List[str]] = None,
    precision: Optional[int] = 3,
    orientation: str = 'horizontal',
    **kwargs: Any
) -> Any:
    """Create a digraph representation of specified tree.

    Each node in the graph represents a node in the tree.

    Non-leaf nodes have labels like ``Column_10 <= 875.9``, which means
    "this node splits on the feature named "Column_10", with threshold 875.9".

    Leaf nodes have labels like ``leaf 2: 0.422``, which means "this node is a
    leaf node, and the predicted value for records that fall into this node
    is 0.422". The number (``2``) is an internal unique identifier and doesn't
    have any special meaning.

    .. note::

        For more information please visit
        https://graphviz.readthedocs.io/en/stable/api.html#digraph.

    Parameters
    ----------
    booster : Booster or LGBMModel
        Booster or LGBMModel instance to be converted.
    tree_index : int, optional (default=0)
        The index of a target tree to convert.
    show_info : list of str, or None, optional (default=None)
        What information should be shown in nodes.

            - ``'split_gain'`` : gain from adding this split to the model
            - ``'internal_value'`` : raw predicted value that would be produced by this node if it was a leaf node
            - ``'internal_count'`` : number of records from the training data that fall into this non-leaf node
            - ``'internal_weight'`` : total weight of all nodes that fall into this non-leaf node
            - ``'leaf_count'`` : number of records from the training data that fall into this leaf node
            - ``'leaf_weight'`` : total weight (sum of hessian) of all observations that fall into this leaf node
            - ``'data_percentage'`` : percentage of training data that fall into this node
    precision : int or None, optional (default=3)
        Used to restrict the display of floating point values to a certain precision.
    orientation : str, optional (default='horizontal')
        Orientation of the tree.
        Can be 'horizontal' or 'vertical'.
    **kwargs
        Other parameters passed to ``Digraph`` constructor.
        Check https://graphviz.readthedocs.io/en/stable/api.html#digraph for the full list of supported parameters.

    Returns
    -------
    graph : graphviz.Digraph
        The digraph representation of specified tree.
    """
    if isinstance(booster, LGBMModel):
        booster = booster.booster_
    elif not isinstance(booster, Booster):
        raise TypeError('booster must be Booster or LGBMModel.')

    model = booster.dump_model()
    tree_infos = model['tree_info']
    if 'feature_names' in model:
        feature_names = model['feature_names']
    else:
        feature_names = None

    monotone_constraints = model.get('monotone_constraints', None)

    if tree_index < len(tree_infos):
        tree_info = tree_infos[tree_index]
    else:
        raise IndexError('tree_index is out of range.')

    if show_info is None:
        show_info = []

    graph = _to_graphviz(tree_info, show_info, feature_names, precision,
                         orientation, monotone_constraints, **kwargs)

    return graph
