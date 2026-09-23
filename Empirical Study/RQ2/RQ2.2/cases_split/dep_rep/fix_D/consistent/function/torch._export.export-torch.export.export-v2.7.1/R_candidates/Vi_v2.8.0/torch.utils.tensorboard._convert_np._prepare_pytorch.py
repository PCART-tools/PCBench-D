def _prepare_pytorch(x: torch.Tensor) -> np.ndarray:
    if x.dtype == torch.bfloat16:
        x = x.to(torch.float16)
    x = x.detach().cpu().numpy()
    return x
