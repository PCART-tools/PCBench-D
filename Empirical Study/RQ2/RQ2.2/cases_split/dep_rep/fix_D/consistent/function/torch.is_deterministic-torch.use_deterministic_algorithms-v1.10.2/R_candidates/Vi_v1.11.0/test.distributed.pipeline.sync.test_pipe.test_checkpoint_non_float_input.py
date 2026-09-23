def test_checkpoint_non_float_input(setup_rpc):
    class ForkNonFloat(nn.Module):
        def forward(self, input):
            return (input * 2, torch.tensor([False]))

    class JoinNonFloat(nn.Module):
        def forward(self, input, non_float):
            return input * 2

    model = nn.Sequential(ForkNonFloat(), JoinNonFloat())
    model = Pipe(model, chunks=1, checkpoint="always")

    input = torch.rand(1, requires_grad=True)
    output = model(input)
    output.backward()
