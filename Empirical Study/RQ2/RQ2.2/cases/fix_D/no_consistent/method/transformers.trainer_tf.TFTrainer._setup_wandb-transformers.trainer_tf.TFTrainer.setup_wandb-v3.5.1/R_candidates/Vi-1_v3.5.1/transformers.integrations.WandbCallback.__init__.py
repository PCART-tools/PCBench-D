    def __init__(self):
        assert _has_wandb, "WandbCallback requires wandb to be installed. Run `pip install wandb`."
        self._initialized = False
