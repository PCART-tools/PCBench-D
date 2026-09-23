class TrainingCheckPoint(TrainingCallback):
    """Checkpointing operation. Users are encouraged to create their own callbacks for
    checkpoint as XGBoost doesn't handle distributed file systems. When checkpointing on
    distributed systems, be sure to know the rank of the worker to avoid multiple
    workers checkpointing to the same place.

    .. versionadded:: 1.3.0

    Since XGBoost 2.1.0, the default format is changed to UBJSON.

    Parameters
    ----------

    directory :
        Output model directory.
    name :
        pattern of output model file.  Models will be saved as name_0.ubj, name_1.ubj,
        name_2.ubj ....
    as_pickle :
        When set to True, all training parameters will be saved in pickle format,
        instead of saving only the model.
    interval :
        Interval of checkpointing.  Checkpointing is slow so setting a larger number can
        reduce performance hit.

    """

    default_format = "ubj"

    def __init__(
        self,
        directory: Union[str, os.PathLike],
        name: str = "model",
        as_pickle: bool = False,
        interval: int = 100,
    ) -> None:
        self._path = os.fspath(directory)
        self._name = name
        self._as_pickle = as_pickle
        self._iterations = interval
        self._epoch = 0  # counter for iterval
        self._start = 0  # beginning iteration
        super().__init__()

    def before_training(self, model: _Model) -> _Model:
        self._start = model.num_boosted_rounds()
        return model

    def after_iteration(
        self, model: _Model, epoch: int, evals_log: TrainingCallback.EvalsLog
    ) -> bool:
        if self._epoch == self._iterations:
            path = os.path.join(
                self._path,
                self._name
                + "_"
                + (str(epoch + self._start))
                + (".pkl" if self._as_pickle else f".{self.default_format}"),
            )
            self._epoch = 0  # reset counter
            if collective.get_rank() == 0:
                # checkpoint using the first worker
                if self._as_pickle:
                    with open(path, "wb") as fd:
                        pickle.dump(model, fd)
                else:
                    model.save_model(path)
        self._epoch += 1
        return False
