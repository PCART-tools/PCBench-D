    def call(self, hidden_states, training=False):
        h = self.wi(hidden_states)
        h = self.act(h)
        h = self.dropout(h, training=training)
        h = self.wo(h)
        return h
