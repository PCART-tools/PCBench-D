def test_detect_checkpointing_recomputing():
    logs = []

    class Detect(nn.Module):
        def forward(self, input):
            logs.append((is_checkpointing(), is_recomputing()))
            return input

    model = Detect()
    input = torch.rand(1, requires_grad=True)

    output = checkpoint(model, input)
    output.backward()

    assert logs == [(True, False), (False, True)]
