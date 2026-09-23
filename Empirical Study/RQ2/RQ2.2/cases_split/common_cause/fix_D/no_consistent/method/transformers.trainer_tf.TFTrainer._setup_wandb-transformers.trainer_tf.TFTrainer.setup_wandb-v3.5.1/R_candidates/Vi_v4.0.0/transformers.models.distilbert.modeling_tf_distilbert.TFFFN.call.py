    def call(self, input, training=False):
        x = self.lin1(input)
        x = self.activation(x)
        x = self.lin2(x)
        x = self.dropout(x, training=training)
        return x
