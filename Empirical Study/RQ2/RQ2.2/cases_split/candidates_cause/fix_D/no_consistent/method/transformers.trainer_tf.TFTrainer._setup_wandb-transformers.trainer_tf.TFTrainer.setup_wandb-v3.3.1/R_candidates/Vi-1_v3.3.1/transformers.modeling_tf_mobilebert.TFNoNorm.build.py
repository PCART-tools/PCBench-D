    def build(self, input_shape):
        self.bias = self.add_weight("bias", shape=[self.feat_size], initializer="zeros")
        self.weight = self.add_weight("weight", shape=[self.feat_size], initializer="ones")
