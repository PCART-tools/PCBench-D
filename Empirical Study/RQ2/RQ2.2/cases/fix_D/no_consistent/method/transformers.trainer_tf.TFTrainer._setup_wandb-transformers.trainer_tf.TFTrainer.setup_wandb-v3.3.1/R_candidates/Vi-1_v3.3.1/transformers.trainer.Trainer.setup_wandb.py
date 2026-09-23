    def setup_wandb(self):
        """
        Setup the optional Weights & Biases (`wandb`) integration.

        One can subclass and override this method to customize the setup if needed. Find more information
        `here <https://docs.wandb.com/huggingface>`__. You can also override the following environment variables:

        Environment:
            WANDB_WATCH:
                (Optional, ["gradients", "all", "false"]) "gradients" by default, set to "false" to disable gradient logging
                or "all" to log gradients and parameters
            WANDB_PROJECT:
                (Optional): str - "huggingface" by default, set this to a custom string to store results in a different project
            WANDB_DISABLED:
                (Optional): boolean - defaults to false, set to "true" to disable wandb entirely
        """
        if hasattr(self, "_setup_wandb"):
            warnings.warn(
                "The `_setup_wandb` method is deprecated and won't be called in a future version, define `setup_wandb` in your subclass.",
                FutureWarning,
            )
            return self._setup_wandb()

        if self.is_world_process_zero():
            logger.info(
                'Automatic Weights & Biases logging enabled, to disable set os.environ["WANDB_DISABLED"] = "true"'
            )
            try:
                combined_dict = {**self.model.config.to_dict(), **self.args.to_sanitized_dict()}
            except AttributeError:
                # in case the model has no config
                combined_dict = {**self.args.to_sanitized_dict()}
            wandb.init(
                project=os.getenv("WANDB_PROJECT", "huggingface"), config=combined_dict, name=self.args.run_name
            )
            # keep track of model topology and gradients, unsupported on TPU
            if not is_torch_tpu_available() and os.getenv("WANDB_WATCH") != "false":
                wandb.watch(
                    self.model, log=os.getenv("WANDB_WATCH", "gradients"), log_freq=max(100, self.args.logging_steps)
                )
