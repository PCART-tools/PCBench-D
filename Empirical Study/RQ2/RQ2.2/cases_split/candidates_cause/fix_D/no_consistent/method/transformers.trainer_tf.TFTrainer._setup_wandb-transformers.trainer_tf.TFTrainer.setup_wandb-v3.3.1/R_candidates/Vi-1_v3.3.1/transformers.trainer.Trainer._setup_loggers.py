    def _setup_loggers(self):
        if self._loggers_initialized:
            return
        if is_wandb_available():
            self.setup_wandb()
        elif os.environ.get("WANDB_DISABLED") != "true":
            logger.info(
                "You are instantiating a Trainer but W&B is not installed. To use wandb logging, "
                "run `pip install wandb; wandb login` see https://docs.wandb.com/huggingface."
            )
        if is_comet_available():
            self.setup_comet()
        elif os.environ.get("COMET_MODE") != "DISABLED":
            logger.info(
                "To use comet_ml logging, run `pip/conda install comet_ml` "
                "see https://www.comet.ml/docs/python-sdk/huggingface/"
            )
        self._loggers_initialized = True
