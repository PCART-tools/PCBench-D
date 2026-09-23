    def on_train_begin(self, args, state, control, model=None, **kwargs):
        hp_search = state.is_hyper_param_search
        if not self._initialized or hp_search:
            print(args.run_name)
            self.setup(args, state, model, reinit=hp_search, **kwargs)
