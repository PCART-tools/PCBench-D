    def __post_init__(self):
        if self.disable_tqdm is None:
            self.disable_tqdm = logger.getEffectiveLevel() > logging.WARN
        if self.evaluate_during_training is not None:
            self.evaluation_strategy = (
                EvaluationStrategy.STEPS if self.evaluate_during_training else EvaluationStrategy.NO
            )
            warnings.warn(
                "The `evaluate_during_training` argument is deprecated in favor of `evaluation_strategy` (which has more options)",
                FutureWarning,
            )
        else:
            self.evaluation_strategy = EvaluationStrategy(self.evaluation_strategy)

        if self.eval_steps is None:
            self.eval_steps = self.logging_steps

        if self.load_best_model_at_end and self.metric_for_best_model is None:
            self.metric_for_best_model = "loss"
        if self.greater_is_better is None and self.metric_for_best_model is not None:
            self.greater_is_better = self.metric_for_best_model not in ["loss", "eval_loss"]
