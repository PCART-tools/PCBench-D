class _SparkXGBSharedReadWrite:
    @staticmethod
    def saveMetadata(
        instance: Union[_SparkXGBEstimator, _SparkXGBModel],
        path: str,
        sc: SparkContext,
        logger: logging.Logger,
        extraMetadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Save the metadata of an xgboost.spark._SparkXGBEstimator or
        xgboost.spark._SparkXGBModel.
        """
        instance._validate_params()
        skipParams = ["callbacks", "xgb_model", "coll_cfg"]
        jsonParams = {}
        for p, v in instance._paramMap.items():  # pylint: disable=protected-access
            if p.name not in skipParams:
                jsonParams[p.name] = v

        extraMetadata = extraMetadata or {}
        callbacks = instance.getOrDefault("callbacks")
        if callbacks is not None:
            logger.warning(
                "The callbacks parameter is saved using cloudpickle and it "
                "is not a fully self-contained format. It may fail to load "
                "with different versions of dependencies."
            )
            serialized_callbacks = base64.encodebytes(
                cloudpickle.dumps(callbacks)
            ).decode("ascii")
            extraMetadata["serialized_callbacks"] = serialized_callbacks
        init_booster = instance.getOrDefault("xgb_model")
        if init_booster is not None:
            extraMetadata["init_booster"] = _INIT_BOOSTER_SAVE_PATH

        if instance.isDefined("coll_cfg"):
            conf: Config = instance.getOrDefault("coll_cfg")
            if conf is not None:
                extraMetadata["coll_cfg"] = asdict(conf)

        DefaultParamsWriter.saveMetadata(
            instance, path, sc, extraMetadata=extraMetadata, paramMap=jsonParams
        )
        if init_booster is not None:
            ser_init_booster = serialize_booster(init_booster)
            save_path = os.path.join(path, _INIT_BOOSTER_SAVE_PATH)
            _get_spark_session().createDataFrame(
                [(ser_init_booster,)], ["init_booster"]
            ).write.parquet(save_path)

    @staticmethod
    def loadMetadataAndInstance(
        pyspark_xgb_cls: Union[Type[_SparkXGBEstimator], Type[_SparkXGBModel]],
        path: str,
        sc: SparkContext,
        logger: logging.Logger,
    ) -> Tuple[Dict[str, Any], Union[_SparkXGBEstimator, _SparkXGBModel]]:
        """
        Load the metadata and the instance of an xgboost.spark._SparkXGBEstimator or
        xgboost.spark._SparkXGBModel.

        :return: a tuple of (metadata, instance)
        """
        metadata = DefaultParamsReader.loadMetadata(
            path, sc, expectedClassName=get_class_name(pyspark_xgb_cls)
        )
        pyspark_xgb = pyspark_xgb_cls()
        DefaultParamsReader.getAndSetParams(pyspark_xgb, metadata)

        if "serialized_callbacks" in metadata:
            serialized_callbacks = metadata["serialized_callbacks"]
            try:
                callbacks = cloudpickle.loads(
                    base64.decodebytes(serialized_callbacks.encode("ascii"))
                )
                pyspark_xgb.set(pyspark_xgb.callbacks, callbacks)  # type: ignore
            except Exception as e:  # pylint: disable=W0703
                logger.warning(
                    f"Fails to load the callbacks param due to {e}. Please set the "
                    "callbacks param manually for the loaded estimator."
                )
        if "coll_cfg" in metadata:
            pyspark_xgb.set_coll_cfg(Config(**metadata["coll_cfg"]))

        if "init_booster" in metadata:
            load_path = os.path.join(path, metadata["init_booster"])
            ser_init_booster = (
                _get_spark_session().read.parquet(load_path).collect()[0].init_booster
            )
            init_booster = deserialize_booster(ser_init_booster)
            pyspark_xgb.set(pyspark_xgb.xgb_model, init_booster)  # type: ignore

        pyspark_xgb._resetUid(metadata["uid"])  # pylint: disable=protected-access
        return metadata, pyspark_xgb
