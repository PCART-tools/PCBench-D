    def forward(self, sequence_output):
        prediction_scores = self.predictions(sequence_output)
        return prediction_scores
