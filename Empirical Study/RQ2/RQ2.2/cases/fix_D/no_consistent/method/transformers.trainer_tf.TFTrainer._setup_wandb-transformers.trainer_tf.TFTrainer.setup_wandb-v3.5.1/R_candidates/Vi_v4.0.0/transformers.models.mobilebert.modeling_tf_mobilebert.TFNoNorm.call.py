    def call(self, inputs: tf.Tensor):
        return inputs * self.weight + self.bias
