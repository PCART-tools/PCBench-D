def test_non_grad_output():
    class ForkNonGrad(nn.Module):
        def forward(self, input):
            return (input * 2, torch.rand(1))

    model = ForkNonGrad()
    input = torch.rand(1, requires_grad=True)

    output = checkpoint(model, input)
    output[0].backward()
