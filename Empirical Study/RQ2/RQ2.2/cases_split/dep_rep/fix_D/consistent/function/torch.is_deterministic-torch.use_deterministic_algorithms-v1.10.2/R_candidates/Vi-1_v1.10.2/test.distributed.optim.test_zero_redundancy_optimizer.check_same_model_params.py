def check_same_model_params(model_a: torch.nn.Module, model_b: torch.nn.Module, message: str = "") -> None:
    for p_a, p_b in zip(model_a.parameters(), model_b.parameters()):
        assert torch.allclose(p_a, p_b, atol=1e-3), f"Model parameters differ\n{p_a} {p_b}\n" + message

    for b_a, b_b in zip(model_a.buffers(), model_b.buffers()):
        assert torch.allclose(b_a, b_b), f"Model buffers differ {b_a} - {b_b}\n" + message
