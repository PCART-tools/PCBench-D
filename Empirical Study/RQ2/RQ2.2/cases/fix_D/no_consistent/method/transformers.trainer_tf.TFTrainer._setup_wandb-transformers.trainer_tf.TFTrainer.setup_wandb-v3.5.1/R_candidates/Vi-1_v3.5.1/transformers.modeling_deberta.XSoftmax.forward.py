    @staticmethod
    def forward(self, input, mask, dim):
        self.dim = dim
        if version.Version(torch.__version__) >= version.Version("1.2.0a"):
            rmask = ~(mask.bool())
        else:
            rmask = (1 - mask).byte()  # This line is not supported by Onnx tracing.

        output = input.masked_fill(rmask, float("-inf"))
        output = torch.softmax(output, self.dim)
        output.masked_fill_(rmask, 0)
        self.save_for_backward(output)
        return output
