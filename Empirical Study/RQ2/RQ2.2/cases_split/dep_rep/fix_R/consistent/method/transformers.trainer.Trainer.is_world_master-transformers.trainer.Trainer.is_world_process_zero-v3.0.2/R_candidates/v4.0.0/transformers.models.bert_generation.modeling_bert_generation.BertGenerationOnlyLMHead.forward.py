    def forward(self, hidden_states):
        logits = self.decoder(hidden_states)
        return logits
