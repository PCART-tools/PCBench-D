@pytest.mark.parametrize("device", devices)
def test_random_in_checkpoint(device):
    dropout = nn.Dropout(p=0.5)

    torch.manual_seed(0)
    x = torch.randn(3, 3, device=device, requires_grad=True)
    y = dropout(x)
    y.norm().backward()

    torch.manual_seed(0)
    chk_x = torch.randn(3, 3, device=device, requires_grad=True)
    chk_y = checkpoint(dropout, chk_x)
    chk_y.norm().backward()

    assert torch.allclose(x.grad, chk_x.grad)
