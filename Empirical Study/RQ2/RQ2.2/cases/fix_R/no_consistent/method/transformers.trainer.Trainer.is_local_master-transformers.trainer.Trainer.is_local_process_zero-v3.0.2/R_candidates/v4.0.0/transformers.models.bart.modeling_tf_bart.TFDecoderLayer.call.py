    def call(
        self,
        x,
        encoder_hidden_states: tf.Tensor,
        encoder_attn_mask=None,
        layer_state=None,
        causal_mask=None,
        decoder_padding_mask=None,
        training=False,
    ) -> Tuple[tf.Tensor, tf.Tensor, Dict[str, tf.Tensor]]:
        """
        Args:
            x (Tensor): input to the layer of shape `(seq_len, batch, embed_dim)`
            encoder_attn_mask (ByteTensor, optional): binary
                ByteTensor of shape `(batch, src_len)` where padding elements are indicated by ``1``.
            need_attn_weights (bool, optional): return attention weights
                for each head (default: return average over heads).

        Returns:

            Tuple containing, encoded output of shape `(seq_len, batch, embed_dim)`, self_attn_weights, layer_state
        """
        residual = x  # Make a copy of the input tensor to add later.
        if layer_state is None:
            layer_state = {}
        if self.normalize_before:
            x = self.self_attn_layer_norm(x)

        # next line mutates layer state and we need a copy of it
        x, self_attn_weights = self.self_attn(
            query=x,
            key=x,
            layer_state=layer_state,
            attn_mask=causal_mask,
            key_padding_mask=decoder_padding_mask,
        )
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)
        x = residual + x
        if not self.normalize_before:
            x = self.self_attn_layer_norm(x)
        # Cross-Attention Block
        residual = x
        if self.normalize_before:
            x = self.encoder_attn_layer_norm(x)
        x, _ = self.encoder_attn(
            query=x,
            key=encoder_hidden_states,
            key_padding_mask=encoder_attn_mask,
            layer_state=layer_state,  # mutates layer state
        )
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)
        x = residual + x
        if not self.normalize_before:
            x = self.encoder_attn_layer_norm(x)
        # Fully Connected
        residual = x
        if self.normalize_before:
            x = self.final_layer_norm(x)
        x = self.activation_fn(self.fc1(x))
        x = tf.nn.dropout(x, rate=self.activation_dropout if training else 0)
        x = self.fc2(x)
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)
        x = residual + x
        if not self.normalize_before:
            x = self.final_layer_norm(x)
        return (
            x,
            self_attn_weights,
            layer_state,
        )  # just self_attn weights for now, following t5, layer_state = cache for decoding
