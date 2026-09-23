    def forward(self, hidden_states):
        return self.logit_fc(hidden_states)
