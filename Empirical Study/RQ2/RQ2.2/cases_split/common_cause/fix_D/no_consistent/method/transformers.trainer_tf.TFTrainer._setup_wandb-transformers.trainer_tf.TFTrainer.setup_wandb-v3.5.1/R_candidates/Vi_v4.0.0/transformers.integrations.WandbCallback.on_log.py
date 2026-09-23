    def on_log(self, args, state, control, model=None, logs=None, **kwargs):
        if not self._initialized:
            self.setup(args, state, model, reinit=False)
        if state.is_world_process_zero:
            logs = rewrite_logs(logs)
            wandb.log(logs, step=state.global_step)
