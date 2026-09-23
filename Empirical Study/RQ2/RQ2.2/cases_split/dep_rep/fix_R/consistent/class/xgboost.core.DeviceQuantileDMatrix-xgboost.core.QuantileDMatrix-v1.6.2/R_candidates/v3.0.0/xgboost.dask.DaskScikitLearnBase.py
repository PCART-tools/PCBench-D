class DaskScikitLearnBase(XGBModel):
    """Base class for implementing scikit-learn interface with Dask"""

    _client = None

    def __init__(self, *, coll_cfg: Optional[CollConfig] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.coll_cfg = coll_cfg

    async def _predict_async(
        self,
        data: _DataT,
        *,
        output_margin: bool,
        validate_features: bool,
        base_margin: Optional[_DaskCollection],
        iteration_range: Optional[IterationRange],
    ) -> Any:
        iteration_range = self._get_iteration_range(iteration_range)
        if self._can_use_inplace_predict():
            predts = await inplace_predict(
                client=self.client,
                model=self.get_booster(),
                data=data,
                iteration_range=iteration_range,
                predict_type="margin" if output_margin else "value",
                missing=self.missing,
                base_margin=base_margin,
                validate_features=validate_features,
            )
            if isinstance(predts, dd.DataFrame):
                predts = predts.to_dask_array()
        else:
            test_dmatrix: DaskDMatrix = await DaskDMatrix(  # type: ignore
                self.client,
                data=data,
                base_margin=base_margin,
                missing=self.missing,
                feature_types=self.feature_types,
            )
            predts = await predict(
                self.client,
                model=self.get_booster(),
                data=test_dmatrix,
                output_margin=output_margin,
                validate_features=validate_features,
                iteration_range=iteration_range,
            )
        return predts

    @_deprecate_positional_args
    def predict(
        self,
        X: _DataT,
        *,
        output_margin: bool = False,
        validate_features: bool = True,
        base_margin: Optional[_DaskCollection] = None,
        iteration_range: Optional[IterationRange] = None,
    ) -> Any:
        return self.client.sync(
            self._predict_async,
            X,
            output_margin=output_margin,
            validate_features=validate_features,
            base_margin=base_margin,
            iteration_range=iteration_range,
        )

    async def _apply_async(
        self,
        X: _DataT,
        iteration_range: Optional[IterationRange] = None,
    ) -> Any:
        iteration_range = self._get_iteration_range(iteration_range)
        test_dmatrix: DaskDMatrix = await DaskDMatrix(  # type: ignore
            self.client,
            data=X,
            missing=self.missing,
            feature_types=self.feature_types,
        )
        predts = await predict(
            self.client,
            model=self.get_booster(),
            data=test_dmatrix,
            pred_leaf=True,
            iteration_range=iteration_range,
        )
        return predts

    def apply(
        self,
        X: _DataT,
        iteration_range: Optional[IterationRange] = None,
    ) -> Any:
        return self.client.sync(self._apply_async, X, iteration_range=iteration_range)

    def __await__(self) -> Awaitable[Any]:
        # Generate a coroutine wrapper to make this class awaitable.
        async def _() -> Awaitable[Any]:
            return self

        return self._client_sync(_).__await__()

    def __getstate__(self) -> Dict:
        this = self.__dict__.copy()
        if "_client" in this:
            del this["_client"]
        return this

    @property
    def client(self) -> "distributed.Client":
        """The dask client used in this model.  The `Client` object can not be
        serialized for transmission, so if task is launched from a worker instead of
        directly from the client process, this attribute needs to be set at that worker.

        """

        client = _get_client(self._client)
        return client

    @client.setter
    def client(self, clt: "distributed.Client") -> None:
        # calling `worker_client' doesn't return the correct `asynchronous` attribute,
        # so we have to pass it ourselves.
        self._asynchronous = clt.asynchronous if clt is not None else False
        self._client = clt

    def _client_sync(self, func: Callable, **kwargs: Any) -> Any:
        """Get the correct client, when method is invoked inside a worker we
        should use `worker_client' instead of default client.

        """

        if self._client is None:
            asynchronous = getattr(self, "_asynchronous", False)
            try:
                distributed.get_worker()
                in_worker = True
            except ValueError:
                in_worker = False
            if in_worker:
                with distributed.worker_client() as client:
                    with _set_worker_client(self, client) as this:
                        ret = this.client.sync(
                            func, **kwargs, asynchronous=asynchronous
                        )
                        return ret
                    return ret

        return self.client.sync(func, **kwargs, asynchronous=self.client.asynchronous)
