    def forward(self, x):
        output = self.conv1d(x)
        return self.act(output)
