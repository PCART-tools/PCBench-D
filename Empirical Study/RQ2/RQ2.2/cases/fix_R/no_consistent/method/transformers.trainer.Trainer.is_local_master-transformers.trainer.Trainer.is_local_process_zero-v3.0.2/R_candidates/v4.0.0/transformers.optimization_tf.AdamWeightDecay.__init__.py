    def __init__(
        self,
        learning_rate: Union[float, tf.keras.optimizers.schedules.LearningRateSchedule] = 0.001,
        beta_1: float = 0.9,
        beta_2: float = 0.999,
        epsilon: float = 1e-7,
        amsgrad: bool = False,
        weight_decay_rate: float = 0.0,
        include_in_weight_decay: Optional[List[str]] = None,
        exclude_from_weight_decay: Optional[List[str]] = None,
        name: str = "AdamWeightDecay",
        **kwargs
    ):
        super().__init__(learning_rate, beta_1, beta_2, epsilon, amsgrad, name, **kwargs)
        self.weight_decay_rate = weight_decay_rate
        self._include_in_weight_decay = include_in_weight_decay
        self._exclude_from_weight_decay = exclude_from_weight_decay
