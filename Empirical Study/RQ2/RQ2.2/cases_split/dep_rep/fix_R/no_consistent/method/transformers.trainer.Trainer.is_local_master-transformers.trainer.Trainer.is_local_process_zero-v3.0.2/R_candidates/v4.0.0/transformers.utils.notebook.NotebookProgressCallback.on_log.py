    def on_log(self, args, state, control, logs=None, **kwargs):
        # Only for when there is no evaluation
        if args.evaluation_strategy == EvaluationStrategy.NO and "loss" in logs:
            values = {"Training Loss": logs["loss"]}
            # First column is necessarily Step sine we're not in epoch eval strategy
            values["Step"] = state.global_step
            self.training_tracker.write_line(values)
