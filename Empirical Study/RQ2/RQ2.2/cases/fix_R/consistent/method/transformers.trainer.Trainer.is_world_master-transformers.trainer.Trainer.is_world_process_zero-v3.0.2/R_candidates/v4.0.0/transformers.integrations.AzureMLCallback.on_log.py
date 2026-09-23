    def on_log(self, args, state, control, logs=None, **kwargs):
        if self.azureml_run:
            for k, v in logs.items():
                if isinstance(v, (int, float)):
                    self.azureml_run.log(k, v, description=k)
