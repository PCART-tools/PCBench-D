def _train(
    client: Client,
    data: _DaskMatrixLike,
    label: _DaskCollection,
    params: Dict[str, Any],
    model_factory: Type[LGBMModel],
    sample_weight: Optional[_DaskVectorLike] = None,
    init_score: Optional[_DaskCollection] = None,
    group: Optional[_DaskVectorLike] = None,
    eval_set: Optional[List[Tuple[_DaskMatrixLike, _DaskCollection]]] = None,
    eval_names: Optional[List[str]] = None,
    eval_sample_weight: Optional[List[_DaskVectorLike]] = None,
    eval_class_weight: Optional[List[Union[dict, str]]] = None,
    eval_init_score: Optional[List[_DaskCollection]] = None,
    eval_group: Optional[List[_DaskVectorLike]] = None,
    eval_metric: Optional[Union[Callable, str, List[Union[Callable, str]]]] = None,
    eval_at: Optional[Iterable[int]] = None,
    **kwargs: Any
) -> LGBMModel:
    """Inner train routine.

    Parameters
    ----------
    client : dask.distributed.Client
        Dask client.
    data : Dask Array or Dask DataFrame of shape = [n_samples, n_features]
        Input feature matrix.
    label : Dask Array, Dask DataFrame or Dask Series of shape = [n_samples]
        The target values (class labels in classification, real numbers in regression).
    params : dict
        Parameters passed to constructor of the local underlying model.
    model_factory : lightgbm.LGBMClassifier, lightgbm.LGBMRegressor, or lightgbm.LGBMRanker class
        Class of the local underlying model.
    sample_weight : Dask Array or Dask Series of shape = [n_samples] or None, optional (default=None)
        Weights of training data.
    init_score : Dask Array or Dask Series of shape = [n_samples] or shape = [n_samples * n_classes] (for multi-class task), or Dask Array or Dask DataFrame of shape = [n_samples, n_classes] (for multi-class task), or None, optional (default=None)
        Init score of training data.
    group : Dask Array or Dask Series or None, optional (default=None)
        Group/query data.
        Only used in the learning-to-rank task.
        sum(group) = n_samples.
        For example, if you have a 100-document dataset with ``group = [10, 20, 40, 10, 10, 10]``, that means that you have 6 groups,
        where the first 10 records are in the first group, records 11-30 are in the second group, records 31-70 are in the third group, etc.
    eval_set : list of (X, y) tuples of Dask data collections, or None, optional (default=None)
        List of (X, y) tuple pairs to use as validation sets.
        Note, that not all workers may receive chunks of every eval set within ``eval_set``. When the returned
        lightgbm estimator is not trained using any chunks of a particular eval set, its corresponding component
        of evals_result_ and best_score_ will be 'not_evaluated'.
    eval_names : list of str, or None, optional (default=None)
        Names of eval_set.
    eval_sample_weight : list of Dask Array or Dask Series, or None, optional (default=None)
        Weights for each validation set in eval_set.
    eval_class_weight : list of dict or str, or None, optional (default=None)
        Class weights, one dict or str for each validation set in eval_set.
    eval_init_score : list of Dask Array, Dask Series or Dask DataFrame (for multi-class task), or None, optional (default=None)
        Initial model score for each validation set in eval_set.
    eval_group : list of Dask Array or Dask Series, or None, optional (default=None)
        Group/query for each validation set in eval_set.
    eval_metric : str, callable, list or None, optional (default=None)
        If str, it should be a built-in evaluation metric to use.
        If callable, it should be a custom evaluation metric, see note below for more details.
        If list, it can be a list of built-in metrics, a list of custom evaluation metrics, or a mix of both.
        In either case, the ``metric`` from the Dask model parameters (or inferred from the objective) will be evaluated and used as well.
        Default: 'l2' for DaskLGBMRegressor, 'binary(multi)_logloss' for DaskLGBMClassifier, 'ndcg' for DaskLGBMRanker.
    eval_at : iterable of int, optional (default=None)
        The evaluation positions of the specified ranking metric.
    **kwargs
        Other parameters passed to ``fit`` method of the local underlying model.

    Returns
    -------
    model : lightgbm.LGBMClassifier, lightgbm.LGBMRegressor, or lightgbm.LGBMRanker class
        Returns fitted underlying model.

    Note
    ----

    This method handles setting up the following network parameters based on information
    about the Dask cluster referenced by ``client``.

    * ``local_listen_port``: port that each LightGBM worker opens a listening socket on,
            to accept connections from other workers. This can differ from LightGBM worker
            to LightGBM worker, but does not have to.
    * ``machines``: a comma-delimited list of all workers in the cluster, in the
            form ``ip:port,ip:port``. If running multiple Dask workers on the same host, use different
            ports for each worker. For example, for ``LocalCluster(n_workers=3)``, you might
            pass ``"127.0.0.1:12400,127.0.0.1:12401,127.0.0.1:12402"``.
    * ``num_machines``: number of LightGBM workers.
    * ``timeout``: time in minutes to wait before closing unused sockets.

    The default behavior of this function is to generate ``machines`` from the list of
    Dask workers which hold some piece of the training data, and to search for an open
    port on each worker to be used as ``local_listen_port``.

    If ``machines`` is provided explicitly in ``params``, this function uses the hosts
    and ports in that list directly, and does not do any searching. This means that if
    any of the Dask workers are missing from the list or any of those ports are not free
    when training starts, training will fail.

    If ``local_listen_port`` is provided in ``params`` and ``machines`` is not, this function
    constructs ``machines`` from the list of Dask workers which hold some piece of the
    training data, assuming that each one will use the same ``local_listen_port``.
    """
    params = deepcopy(params)

    # capture whether local_listen_port or its aliases were provided
    listen_port_in_params = any(
        alias in params for alias in _ConfigAliases.get("local_listen_port")
    )

    # capture whether machines or its aliases were provided
    machines_in_params = any(
        alias in params for alias in _ConfigAliases.get("machines")
    )

    params = _choose_param_value(
        main_param_name="tree_learner",
        params=params,
        default_value="data"
    )
    allowed_tree_learners = {
        'data',
        'data_parallel',
        'feature',
        'feature_parallel',
        'voting',
        'voting_parallel'
    }
    if params["tree_learner"] not in allowed_tree_learners:
        _log_warning(f'Parameter tree_learner set to {params["tree_learner"]}, which is not allowed. Using "data" as default')
        params['tree_learner'] = 'data'

    # Some passed-in parameters can be removed:
    #   * 'num_machines': set automatically from Dask worker list
    #   * 'num_threads': overridden to match nthreads on each Dask process
    for param_alias in _ConfigAliases.get('num_machines', 'num_threads'):
        if param_alias in params:
            _log_warning(f"Parameter {param_alias} will be ignored.")
            params.pop(param_alias)

    # Split arrays/dataframes into parts. Arrange parts into dicts to enforce co-locality
    data_parts = _split_to_parts(data=data, is_matrix=True)
    label_parts = _split_to_parts(data=label, is_matrix=False)
    parts = [{'data': x, 'label': y} for (x, y) in zip(data_parts, label_parts)]
    n_parts = len(parts)

    if sample_weight is not None:
        weight_parts = _split_to_parts(data=sample_weight, is_matrix=False)
        for i in range(n_parts):
            parts[i]['weight'] = weight_parts[i]

    if group is not None:
        group_parts = _split_to_parts(data=group, is_matrix=False)
        for i in range(n_parts):
            parts[i]['group'] = group_parts[i]

    if init_score is not None:
        init_score_parts = _split_to_parts(data=init_score, is_matrix=False)
        for i in range(n_parts):
            parts[i]['init_score'] = init_score_parts[i]

    # evals_set will to be re-constructed into smaller lists of (X, y) tuples, where
    # X and y are each delayed sub-lists of original eval dask Collections.
    if eval_set:
        # find maximum number of parts in an individual eval set so that we can
        # pad eval sets when they come in different sizes.
        n_largest_eval_parts = max(x[0].npartitions for x in eval_set)

        eval_sets = defaultdict(list)
        if eval_sample_weight:
            eval_sample_weights = defaultdict(list)
        if eval_group:
            eval_groups = defaultdict(list)
        if eval_init_score:
            eval_init_scores = defaultdict(list)

        for i, (X_eval, y_eval) in enumerate(eval_set):
            n_this_eval_parts = X_eval.npartitions

            # when individual eval set is equivalent to training data, skip recomputing parts.
            if X_eval is data and y_eval is label:
                for parts_idx in range(n_parts):
                    eval_sets[parts_idx].append(_DatasetNames.TRAINSET)
            else:
                eval_x_parts = _split_to_parts(data=X_eval, is_matrix=True)
                eval_y_parts = _split_to_parts(data=y_eval, is_matrix=False)
                for j in range(n_largest_eval_parts):
                    parts_idx = j % n_parts

                    # add None-padding for individual eval_set member if it is smaller than the largest member.
                    if j < n_this_eval_parts:
                        x_e = eval_x_parts[j]
                        y_e = eval_y_parts[j]
                    else:
                        x_e = None
                        y_e = None

                    if j < n_parts:
                        # first time a chunk of this eval set is added to this part.
                        eval_sets[parts_idx].append(([x_e], [y_e]))
                    else:
                        # append additional chunks of this eval set to this part.
                        eval_sets[parts_idx][-1][0].append(x_e)
                        eval_sets[parts_idx][-1][1].append(y_e)

            if eval_sample_weight:
                if eval_sample_weight[i] is sample_weight:
                    for parts_idx in range(n_parts):
                        eval_sample_weights[parts_idx].append(_DatasetNames.SAMPLE_WEIGHT)
                else:
                    eval_w_parts = _split_to_parts(data=eval_sample_weight[i], is_matrix=False)

                    # ensure that all evaluation parts map uniquely to one part.
                    for j in range(n_largest_eval_parts):
                        if j < n_this_eval_parts:
                            w_e = eval_w_parts[j]
                        else:
                            w_e = None

                        parts_idx = j % n_parts
                        if j < n_parts:
                            eval_sample_weights[parts_idx].append([w_e])
                        else:
                            eval_sample_weights[parts_idx][-1].append(w_e)

            if eval_init_score:
                if eval_init_score[i] is init_score:
                    for parts_idx in range(n_parts):
                        eval_init_scores[parts_idx].append(_DatasetNames.INIT_SCORE)
                else:
                    eval_init_score_parts = _split_to_parts(data=eval_init_score[i], is_matrix=False)
                    for j in range(n_largest_eval_parts):
                        if j < n_this_eval_parts:
                            init_score_e = eval_init_score_parts[j]
                        else:
                            init_score_e = None

                        parts_idx = j % n_parts
                        if j < n_parts:
                            eval_init_scores[parts_idx].append([init_score_e])
                        else:
                            eval_init_scores[parts_idx][-1].append(init_score_e)

            if eval_group:
                if eval_group[i] is group:
                    for parts_idx in range(n_parts):
                        eval_groups[parts_idx].append(_DatasetNames.GROUP)
                else:
                    eval_g_parts = _split_to_parts(data=eval_group[i], is_matrix=False)
                    for j in range(n_largest_eval_parts):
                        if j < n_this_eval_parts:
                            g_e = eval_g_parts[j]
                        else:
                            g_e = None

                        parts_idx = j % n_parts
                        if j < n_parts:
                            eval_groups[parts_idx].append([g_e])
                        else:
                            eval_groups[parts_idx][-1].append(g_e)

        # assign sub-eval_set components to worker parts.
        for parts_idx, e_set in eval_sets.items():
            parts[parts_idx]['eval_set'] = e_set
            if eval_sample_weight:
                parts[parts_idx]['eval_sample_weight'] = eval_sample_weights[parts_idx]
            if eval_init_score:
                parts[parts_idx]['eval_init_score'] = eval_init_scores[parts_idx]
            if eval_group:
                parts[parts_idx]['eval_group'] = eval_groups[parts_idx]

    # Start computation in the background
    parts = list(map(delayed, parts))
    parts = client.compute(parts)
    wait(parts)

    for part in parts:
        if part.status == 'error':  # type: ignore
            return part  # trigger error locally

    # Find locations of all parts and map them to particular Dask workers
    key_to_part_dict = {part.key: part for part in parts}  # type: ignore
    who_has = client.who_has(parts)
    worker_map = defaultdict(list)
    for key, workers in who_has.items():
        worker_map[next(iter(workers))].append(key_to_part_dict[key])

    # Check that all workers were provided some of eval_set. Otherwise warn user that validation
    # data artifacts may not be populated depending on worker returning final estimator.
    if eval_set:
        for worker in worker_map:
            has_eval_set = False
            for part in worker_map[worker]:
                if 'eval_set' in part.result():
                    has_eval_set = True
                    break

            if not has_eval_set:
                _log_warning(
                    f"Worker {worker} was not allocated eval_set data. Therefore evals_result_ and best_score_ data may be unreliable. "
                    "Try rebalancing data across workers."
                )

    # assign general validation set settings to fit kwargs.
    if eval_names:
        kwargs['eval_names'] = eval_names
    if eval_class_weight:
        kwargs['eval_class_weight'] = eval_class_weight
    if eval_metric:
        kwargs['eval_metric'] = eval_metric
    if eval_at:
        kwargs['eval_at'] = eval_at

    master_worker = next(iter(worker_map))
    worker_ncores = client.ncores()

    # resolve aliases for network parameters and pop the result off params.
    # these values are added back in calls to `_train_part()`
    params = _choose_param_value(
        main_param_name="local_listen_port",
        params=params,
        default_value=12400
    )
    local_listen_port = params.pop("local_listen_port")

    params = _choose_param_value(
        main_param_name="machines",
        params=params,
        default_value=None
    )
    machines = params.pop("machines")

    # figure out network params
    worker_addresses = worker_map.keys()
    if machines is not None:
        _log_info("Using passed-in 'machines' parameter")
        worker_address_to_port = _machines_to_worker_map(
            machines=machines,
            worker_addresses=worker_addresses
        )
    else:
        if listen_port_in_params:
            _log_info("Using passed-in 'local_listen_port' for all workers")
            unique_hosts = set(urlparse(a).hostname for a in worker_addresses)
            if len(unique_hosts) < len(worker_addresses):
                msg = (
                    "'local_listen_port' was provided in Dask training parameters, but at least one "
                    "machine in the cluster has multiple Dask worker processes running on it. Please omit "
                    "'local_listen_port' or pass 'machines'."
                )
                raise LightGBMError(msg)

            worker_address_to_port = {
                address: local_listen_port
                for address in worker_addresses
            }
        else:
            _log_info("Finding random open ports for workers")
            host_to_workers = _group_workers_by_host(worker_map.keys())
            worker_address_to_port = _assign_open_ports_to_workers(client, host_to_workers)

        machines = ','.join([
            f'{urlparse(worker_address).hostname}:{port}'
            for worker_address, port
            in worker_address_to_port.items()
        ])

    num_machines = len(worker_address_to_port)

    # Tell each worker to train on the parts that it has locally
    #
    # This code treats ``_train_part()`` calls as not "pure" because:
    #     1. there is randomness in the training process unless parameters ``seed``
    #        and ``deterministic`` are set
    #     2. even with those parameters set, the output of one ``_train_part()`` call
    #        relies on global state (it and all the other LightGBM training processes
    #        coordinate with each other)
    futures_classifiers = [
        client.submit(
            _train_part,
            model_factory=model_factory,
            params={**params, 'num_threads': worker_ncores[worker]},
            list_of_parts=list_of_parts,
            machines=machines,
            local_listen_port=worker_address_to_port[worker],
            num_machines=num_machines,
            time_out=params.get('time_out', 120),
            return_model=(worker == master_worker),
            workers=[worker],
            allow_other_workers=False,
            pure=False,
            **kwargs
        )
        for worker, list_of_parts in worker_map.items()
    ]

    results = client.gather(futures_classifiers)
    results = [v for v in results if v]
    model = results[0]

    # if network parameters were changed during training, remove them from the
    # returned model so that they're generated dynamically on every run based
    # on the Dask cluster you're connected to and which workers have pieces of
    # the training data
    if not listen_port_in_params:
        for param in _ConfigAliases.get('local_listen_port'):
            model._other_params.pop(param, None)

    if not machines_in_params:
        for param in _ConfigAliases.get('machines'):
            model._other_params.pop(param, None)

    for param in _ConfigAliases.get('num_machines', 'timeout'):
        model._other_params.pop(param, None)

    return model
