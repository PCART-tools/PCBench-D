    def load_dpr_model(self):
        model = DPRContextEncoder(DPRConfig(**BertConfig.get_config_dict("bert-base-uncased")[0]))
        print("Loading DPR biencoder from {}".format(self.src_file))
        saved_state = load_states_from_checkpoint(self.src_file)
        encoder, prefix = model.ctx_encoder, "ctx_model."
        # Fix changes from https://github.com/huggingface/transformers/commit/614fef1691edb806de976756d4948ecbcd0c0ca3
        state_dict = {"bert_model.embeddings.position_ids": model.ctx_encoder.bert_model.embeddings.position_ids}
        for key, value in saved_state.model_dict.items():
            if key.startswith(prefix):
                key = key[len(prefix) :]
                if not key.startswith("encode_proj."):
                    key = "bert_model." + key
                state_dict[key] = value
        encoder.load_state_dict(state_dict)
        return model
