    def init_attention_inputs(self, input_embeds, attention_mask=None, token_type_ids=None, training=False):
        """ Returns the attention inputs associated to the inputs of the model. """
        # input_embeds has shape batch_size x seq_len x d_model
        # attention_mask and token_type_ids have shape batch_size x seq_len
        self.pooling_mult = 1
        self.seq_len = seq_len = input_embeds.shape[1]
        position_embeds = self.get_position_embeds(seq_len, dtype=input_embeds.dtype, training=training)
        token_type_mat = self.token_type_ids_to_mat(token_type_ids) if token_type_ids is not None else None
        cls_mask = (
            tf.pad(tf.ones([seq_len - 1, seq_len - 1], dtype=input_embeds.dtype), [[1, 0], [1, 0]])
            if self.separate_cls
            else None
        )
        return (position_embeds, token_type_mat, attention_mask, cls_mask)
