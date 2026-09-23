class DaskDMatrix:
    # pylint: disable=too-many-instance-attributes
    """DMatrix holding on references to Dask DataFrame or Dask Array.  Constructing a
    `DaskDMatrix` forces all lazy computation to be carried out.  Wait for the input
    data explicitly if you want to see actual computation of constructing `DaskDMatrix`.

    See doc for :py:obj:`xgboost.DMatrix` constructor for other parameters.  DaskDMatrix
    accepts only dask collection.

    .. note::

        `DaskDMatrix` does not repartition or move data between workers.  It's the
        caller's responsibility to balance the data.

    .. note::

        For aligning partitions with ranking query groups, use the
        :py:class:`DaskXGBRanker` and its ``allow_group_split`` option.

    .. versionadded:: 1.0.0

    Parameters
    ----------
    client :
        Specify the dask client used for training.  Use default client returned from
        dask if it's set to None.

    """

    @_deprecate_positional_args
    def __init__(
        self,
        client: Optional["distributed.Client"],
        data: _DataT,
        label: Optional[_DaskCollection] = None,
        *,
        weight: Optional[_DaskCollection] = None,
        base_margin: Optional[_DaskCollection] = None,
        missing: Optional[float] = None,
        silent: bool = False,  # pylint: disable=unused-argument
        feature_names: Optional[FeatureNames] = None,
        feature_types: Optional[FeatureTypes] = None,
        group: Optional[_DaskCollection] = None,
        qid: Optional[_DaskCollection] = None,
        label_lower_bound: Optional[_DaskCollection] = None,
        label_upper_bound: Optional[_DaskCollection] = None,
        feature_weights: Optional[_DaskCollection] = None,
        enable_categorical: bool = False,
    ) -> None:
        client = _get_client(client)

        self.feature_names = feature_names
        self.feature_types = feature_types
        self.missing = missing if missing is not None else numpy.nan
        self.enable_categorical = enable_categorical

        if qid is not None and weight is not None:
            raise NotImplementedError("per-group weight is not implemented.")
        if group is not None:
            raise NotImplementedError(
                "group structure is not implemented, use qid instead."
            )

        if len(data.shape) != 2:
            raise ValueError(f"Expecting 2 dimensional input, got: {data.shape}")

        if not isinstance(data, (dd.DataFrame, da.Array)):
            raise TypeError(_expect((dd.DataFrame, da.Array), type(data)))
        if not isinstance(label, (dd.DataFrame, da.Array, dd.Series, type(None))):
            raise TypeError(_expect((dd.DataFrame, da.Array, dd.Series), type(label)))

        self._n_cols = data.shape[1]
        assert isinstance(self._n_cols, int)
        self.worker_map: Dict[str, List[Future]] = defaultdict(list)
        self.is_quantile: bool = False

        self._init = client.sync(
            self._map_local_data,
            client=client,
            data=data,
            label=label,
            weights=weight,
            base_margin=base_margin,
            qid=qid,
            feature_weights=feature_weights,
            label_lower_bound=label_lower_bound,
            label_upper_bound=label_upper_bound,
        )

    def __await__(self) -> Generator:
        return self._init.__await__()

    async def _map_local_data(
        self,
        *,
        client: "distributed.Client",
        data: _DataT,
        label: Optional[_DaskCollection] = None,
        weights: Optional[_DaskCollection] = None,
        base_margin: Optional[_DaskCollection] = None,
        qid: Optional[_DaskCollection] = None,
        feature_weights: Optional[_DaskCollection] = None,
        label_lower_bound: Optional[_DaskCollection] = None,
        label_upper_bound: Optional[_DaskCollection] = None,
    ) -> "DaskDMatrix":
        """Obtain references to local data."""

        def inconsistent(
            left: List[Any], left_name: str, right: List[Any], right_name: str
        ) -> str:
            msg = (
                f"Partitions between {left_name} and {right_name} are not "
                f"consistent: {len(left)} != {len(right)}.  "
                f"Please try to repartition/rechunk your data."
            )
            return msg

        def to_futures(d: _DaskCollection) -> List[Future]:
            """Breaking data into partitions."""
            d = client.persist(d)
            if (
                hasattr(d.partitions, "shape")
                and len(d.partitions.shape) > 1
                and d.partitions.shape[1] > 1
            ):
                raise ValueError(
                    "Data should be"
                    " partitioned by row. To avoid this specify the number"
                    " of columns for your dask Array explicitly. e.g."
                    " chunks=(partition_size, -1])"
                )
            return client.futures_of(d)

        def flatten_meta(meta: Optional[_DaskCollection]) -> Optional[List[Future]]:
            if meta is not None:
                meta_parts: List[Future] = to_futures(meta)
                return meta_parts
            return None

        X_parts = to_futures(data)
        y_parts = flatten_meta(label)
        w_parts = flatten_meta(weights)
        margin_parts = flatten_meta(base_margin)
        qid_parts = flatten_meta(qid)
        ll_parts = flatten_meta(label_lower_bound)
        lu_parts = flatten_meta(label_upper_bound)

        parts: Dict[str, List[Future]] = {"data": X_parts}

        def append_meta(m_parts: Optional[List[Future]], name: str) -> None:
            if m_parts is not None:
                assert len(X_parts) == len(m_parts), inconsistent(
                    X_parts, "X", m_parts, name
                )
                parts[name] = m_parts

        append_meta(y_parts, "label")
        append_meta(w_parts, "weight")
        append_meta(margin_parts, "base_margin")
        append_meta(qid_parts, "qid")
        append_meta(ll_parts, "label_lower_bound")
        append_meta(lu_parts, "label_upper_bound")
        # At this point, `parts` looks like:
        # [(x0, x1, ..), (y0, y1, ..), ..] in future form

        # turn into list of dictionaries.
        packed_parts: List[Dict[str, Future]] = []
        for i in range(len(X_parts)):
            part_dict: Dict[str, Future] = {}
            for key, value in parts.items():
                part_dict[key] = value[i]
            packed_parts.append(part_dict)

        # delay the zipped result
        # pylint: disable=no-member
        delayed_parts: List[Delayed] = list(map(dask.delayed, packed_parts))
        # At this point, the mental model should look like:
        # [{"data": x0, "label": y0, ..}, {"data": x1, "label": y1, ..}, ..]

        # Convert delayed objects into futures and make sure they are realized
        #
        # This also makes partitions to align (co-locate) on workers (X_0, y_0 should be
        # on the same worker).
        fut_parts: List[Future] = client.compute(delayed_parts)
        await distributed.wait(fut_parts)  # async wait for parts to be computed

        for part in fut_parts:
            # Each part is [{"data": x0, "label": y0, ..}, ...] in future form.
            assert part.status == "finished", part.status

        # Preserving the partition order for prediction.
        self.partition_order = {}
        for i, part in enumerate(fut_parts):
            self.partition_order[part.key] = i

        key_to_partition = {part.key: part for part in fut_parts}
        who_has: Dict[str, Tuple[str, ...]] = await client.scheduler.who_has(
            keys=[part.key for part in fut_parts]
        )

        worker_map: Dict[str, List[Future]] = defaultdict(list)

        for key, workers in who_has.items():
            worker_map[next(iter(workers))].append(key_to_partition[key])

        self.worker_map = worker_map

        if feature_weights is None:
            self.feature_weights = None
        else:
            self.feature_weights = await client.compute(feature_weights).result()

        return self

    def _create_fn_args(self, worker_addr: str) -> Dict[str, Any]:
        """Create a dictionary of objects that can be pickled for function
        arguments.

        """
        return {
            "feature_names": self.feature_names,
            "feature_types": self.feature_types,
            "feature_weights": self.feature_weights,
            "missing": self.missing,
            "enable_categorical": self.enable_categorical,
            "parts": self.worker_map.get(worker_addr, None),
            "is_quantile": self.is_quantile,
        }

    def num_col(self) -> int:
        """Get the number of columns (features) in the DMatrix.

        Returns
        -------
        number of columns
        """
        return self._n_cols
