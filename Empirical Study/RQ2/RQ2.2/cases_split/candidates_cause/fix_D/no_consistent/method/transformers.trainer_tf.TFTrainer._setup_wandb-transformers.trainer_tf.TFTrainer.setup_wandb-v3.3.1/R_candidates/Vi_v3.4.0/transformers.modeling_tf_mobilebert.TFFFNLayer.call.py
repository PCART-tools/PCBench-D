    def call(self, hidden_states):
        intermediate_output = self.intermediate(hidden_states)
        layer_outputs = self.mobilebert_output(intermediate_output, hidden_states)
        return layer_outputs
