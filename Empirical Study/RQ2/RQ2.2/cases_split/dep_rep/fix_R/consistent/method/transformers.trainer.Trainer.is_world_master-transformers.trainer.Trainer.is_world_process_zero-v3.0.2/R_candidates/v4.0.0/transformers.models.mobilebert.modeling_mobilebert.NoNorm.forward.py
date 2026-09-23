    def forward(self, input_tensor):
        return input_tensor * self.weight + self.bias
