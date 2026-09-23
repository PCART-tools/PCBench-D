    def call(self, features):
        x = self.dense(features)
        x = self.act(x)
        x = self.layer_norm(x)

        # project back to size of vocabulary with bias
        x = self.decoder(x, mode="linear") + self.bias

        return x
