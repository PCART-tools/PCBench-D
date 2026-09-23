class ResetStrategy(xgb.callback.TrainingCallback):
    """Callback for testing multi-output."""

    def after_iteration(self, model: xgb.Booster, epoch: int, evals_log: dict) -> bool:
        if epoch % 2 == 0:
            model.set_param({"multi_strategy": "multi_output_tree"})
        else:
            model.set_param({"multi_strategy": "one_output_per_tree"})
        return False
