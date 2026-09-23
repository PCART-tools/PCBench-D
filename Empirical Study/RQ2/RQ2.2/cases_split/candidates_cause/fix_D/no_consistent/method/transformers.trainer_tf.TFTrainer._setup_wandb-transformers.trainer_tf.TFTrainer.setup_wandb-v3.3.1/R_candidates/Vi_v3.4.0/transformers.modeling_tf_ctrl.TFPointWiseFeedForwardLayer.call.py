    def call(self, inputs, trainable=False):
        dense_0_output = self.dense_0(inputs)
        dense_2_output = self.dense_2(dense_0_output)

        return dense_2_output
