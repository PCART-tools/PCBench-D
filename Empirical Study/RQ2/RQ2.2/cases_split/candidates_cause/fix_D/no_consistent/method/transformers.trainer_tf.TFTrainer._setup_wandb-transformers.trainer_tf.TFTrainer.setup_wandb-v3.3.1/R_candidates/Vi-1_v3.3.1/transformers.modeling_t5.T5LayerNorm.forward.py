    def forward(self, x):
        # layer norm should always be calculated in float32
        variance = x.to(torch.float32).pow(2).mean(-1, keepdim=True)
        x = x / torch.sqrt(variance + self.variance_epsilon)

        if self.weight.dtype == torch.float16:
            x = x.to(torch.float16)
        return self.weight * x
