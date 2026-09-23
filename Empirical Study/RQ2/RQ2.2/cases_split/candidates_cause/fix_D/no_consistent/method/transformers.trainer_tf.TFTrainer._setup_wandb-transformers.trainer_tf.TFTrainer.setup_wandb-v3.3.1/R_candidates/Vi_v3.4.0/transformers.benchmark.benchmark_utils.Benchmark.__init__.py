    def __init__(self, args: BenchmarkArguments = None, configs: PretrainedConfig = None):
        self.args = args
        if configs is None:
            self.config_dict = {
                model_name: AutoConfig.from_pretrained(model_name) for model_name in self.args.model_names
            }
        else:
            self.config_dict = {model_name: config for model_name, config in zip(self.args.model_names, configs)}

        if self.args.memory and os.getenv("TRANSFORMERS_USE_MULTIPROCESSING") == 0:
            logger.warning(
                "Memory consumption will not be measured accurately if `args.multi_process` is set to `False.` The flag 'TRANSFORMERS_USE_MULTIPROCESSING' should only be disabled for debugging / testing."
            )

        self._print_fn = None
        self._framework_version = None
        self._environment_info = None
