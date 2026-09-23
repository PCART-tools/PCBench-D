def test_use_grad():
    tensor = torch.rand(1, requires_grad=True)
    portal = Portal(tensor, tensor_life=1)

    portal.put_grad(tensor)
    assert portal.use_grad() is tensor

    # Gradient in a portal is ephemeral.
    with pytest.raises(RuntimeError):
        portal.use_grad()
