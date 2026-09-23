    def call(self, inputs: tf.Tensor, mode: str = "embedding") -> tf.Tensor:
        """
        Get token embeddings of inputs or decode final hidden state.

        Args:
            inputs (:obj:`tf.Tensor`):
                In embedding mode, should be an int64 tensor with shape :obj:`[batch_size, length]`.

                In linear mode, should be a float tensor with shape :obj:`[batch_size, length, hidden_size]`.
            mode (:obj:`str`, defaults to :obj:`"embedding"`):
               A valid value is either :obj:`"embedding"` or :obj:`"linear"`, the first one indicates that the layer
               should be used as an embedding layer, the second one that the layer should be used as a linear decoder.

        Returns:
            :obj:`tf.Tensor`: In embedding mode, the output is a float32 embedding tensor, with shape
            :obj:`[batch_size, length, embedding_size]`.

            In linear mode, the output is a float32 with shape :obj:`[batch_size, length, vocab_size]`.

        Raises:
            ValueError: if :obj:`mode` is not valid.

        Shared weights logic is adapted from `here
        <https://github.com/tensorflow/models/blob/a009f4fb9d2fc4949e32192a944688925ef78659/official/transformer/v2/embedding_layer.py#L24>`__.
        """
        if mode == "embedding":
            return self._embedding(inputs)
        elif mode == "linear":
            return self._linear(inputs)
        else:
            raise ValueError("mode {} is not valid.".format(mode))
