@pytest.mark.xfail(strict=True)
def test_inplace_on_not_requires_grad(setup_rpc):
    # In-place operation on a tensor not requiring grad doesn't cause a
    # RuntimeError. Currently, we cannot detect this case.
    model = nn.Sequential(nn.ReLU(inplace=True))
    model = Pipe(model, [1], devices=["cpu"], checkpoint="always")

    x = torch.rand(1)
    y = model(x).local_value()
    del model

    message = r"a leaf Variable that requires grad .* used in an in-place operation."
    with pytest.raises(RuntimeError, match=message):
        y.backward()
