def plot_metric(
    booster: Union[Dict, LGBMModel],
    metric: Optional[str] = None,
    dataset_names: Optional[List[str]] = None,
    ax=None,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
    title: Optional[str] = 'Metric during training',
    xlabel: Optional[str] = 'Iterations',
    ylabel: Optional[str] = '@metric@',
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    grid: bool = True
) -> Any:
    """Plot one metric during training.

    Parameters
    ----------
    booster : dict or LGBMModel
        Dictionary returned from ``lightgbm.train()`` or LGBMModel instance.
    metric : str or None, optional (default=None)
        The metric name to plot.
        Only one metric supported because different metrics have various scales.
        If None, first metric picked from dictionary (according to hashcode).
    dataset_names : list of str, or None, optional (default=None)
        List of the dataset names which are used to calculate metric to plot.
        If None, all datasets are used.
    ax : matplotlib.axes.Axes or None, optional (default=None)
        Target axes instance.
        If None, new figure and axes will be created.
    xlim : tuple of 2 elements or None, optional (default=None)
        Tuple passed to ``ax.xlim()``.
    ylim : tuple of 2 elements or None, optional (default=None)
        Tuple passed to ``ax.ylim()``.
    title : str or None, optional (default="Metric during training")
        Axes title.
        If None, title is disabled.
    xlabel : str or None, optional (default="Iterations")
        X-axis title label.
        If None, title is disabled.
    ylabel : str or None, optional (default="@metric@")
        Y-axis title label.
        If 'auto', metric name is used.
        If None, title is disabled.
        @metric@ placeholder can be used, and it will be replaced with metric name.
    figsize : tuple of 2 elements or None, optional (default=None)
        Figure size.
    dpi : int or None, optional (default=None)
        Resolution of the figure.
    grid : bool, optional (default=True)
        Whether to add a grid for axes.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The plot with metric's history over the training.
    """
    if MATPLOTLIB_INSTALLED:
        import matplotlib.pyplot as plt
    else:
        raise ImportError('You must install matplotlib and restart your session to plot metric.')

    if isinstance(booster, LGBMModel):
        eval_results = deepcopy(booster.evals_result_)
    elif isinstance(booster, dict):
        eval_results = deepcopy(booster)
    elif isinstance(booster, Booster):
        raise TypeError("booster must be dict or LGBMModel. To use plot_metric with Booster type, first record the metrics using record_evaluation callback then pass that to plot_metric as argument `booster`")
    else:
        raise TypeError('booster must be dict or LGBMModel.')

    num_data = len(eval_results)

    if not num_data:
        raise ValueError('eval results cannot be empty.')

    if ax is None:
        if figsize is not None:
            _check_not_tuple_of_2_elements(figsize, 'figsize')
        _, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    if dataset_names is None:
        dataset_names = iter(eval_results.keys())
    elif not isinstance(dataset_names, (list, tuple, set)) or not dataset_names:
        raise ValueError('dataset_names should be iterable and cannot be empty')
    else:
        dataset_names = iter(dataset_names)

    name = next(dataset_names)  # take one as sample
    metrics_for_one = eval_results[name]
    num_metric = len(metrics_for_one)
    if metric is None:
        if num_metric > 1:
            _log_warning("More than one metric available, picking one to plot.")
        metric, results = metrics_for_one.popitem()
    else:
        if metric not in metrics_for_one:
            raise KeyError('No given metric in eval results.')
        results = metrics_for_one[metric]
    num_iteration = len(results)
    max_result = max(results)
    min_result = min(results)
    x_ = range(num_iteration)
    ax.plot(x_, results, label=name)

    for name in dataset_names:
        metrics_for_one = eval_results[name]
        results = metrics_for_one[metric]
        max_result = max(max(results), max_result)
        min_result = min(min(results), min_result)
        ax.plot(x_, results, label=name)

    ax.legend(loc='best')

    if xlim is not None:
        _check_not_tuple_of_2_elements(xlim, 'xlim')
    else:
        xlim = (0, num_iteration)
    ax.set_xlim(xlim)

    if ylim is not None:
        _check_not_tuple_of_2_elements(ylim, 'ylim')
    else:
        range_result = max_result - min_result
        ylim = (min_result - range_result * 0.2, max_result + range_result * 0.2)
    ax.set_ylim(ylim)

    if ylabel == 'auto':
        _log_warning("'auto' value of 'ylabel' argument is deprecated and will be removed in a future release of LightGBM. "
                     "Use '@metric@' placeholder instead.")
        ylabel = '@metric@'

    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ylabel = ylabel.replace('@metric@', metric)
        ax.set_ylabel(ylabel)
    ax.grid(grid)
    return ax
