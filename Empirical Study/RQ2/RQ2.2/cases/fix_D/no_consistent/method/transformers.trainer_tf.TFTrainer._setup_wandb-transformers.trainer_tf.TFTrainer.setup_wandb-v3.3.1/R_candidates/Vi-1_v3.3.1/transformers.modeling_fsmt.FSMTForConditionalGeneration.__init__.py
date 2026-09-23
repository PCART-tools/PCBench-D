    def __init__(self, config: FSMTConfig):
        super().__init__(config)
        base_model = FSMTModel(config)
        self.model = base_model
