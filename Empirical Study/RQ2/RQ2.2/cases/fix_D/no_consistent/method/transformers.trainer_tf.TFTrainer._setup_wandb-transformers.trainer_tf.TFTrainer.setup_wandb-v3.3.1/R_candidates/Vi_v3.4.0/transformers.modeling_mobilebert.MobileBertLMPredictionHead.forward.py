    def forward(self, hidden_states):
        hidden_states = self.transform(hidden_states)
        hidden_states = hidden_states.matmul(torch.cat([self.decoder.weight.t(), self.dense.weight], dim=0))
        hidden_states += self.bias
        return hidden_states
