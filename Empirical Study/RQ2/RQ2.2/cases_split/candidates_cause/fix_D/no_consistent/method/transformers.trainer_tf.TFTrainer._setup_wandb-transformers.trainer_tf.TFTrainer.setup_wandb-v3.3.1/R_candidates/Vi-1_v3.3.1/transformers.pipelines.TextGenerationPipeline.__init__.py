    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_model_type(self.ALLOWED_MODELS)
