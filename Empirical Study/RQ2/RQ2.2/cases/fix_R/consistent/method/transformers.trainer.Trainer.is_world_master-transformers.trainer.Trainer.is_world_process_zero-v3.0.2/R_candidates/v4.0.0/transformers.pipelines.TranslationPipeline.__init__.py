    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_model_type(
            TF_MODEL_WITH_LM_HEAD_MAPPING if self.framework == "tf" else MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING
        )
