def test_multi_sequence_input(setup_rpc):
    class MultiSeq(nn.Module):
        def forward(self, tup1, tup2):
            return tup1, tup2

    model = Pipe(nn.Sequential(MultiSeq()))
    with pytest.raises(TypeError):
        model(
            [torch.rand(10), torch.rand(10)],
            [torch.rand(10), torch.rand(10)]
        )
