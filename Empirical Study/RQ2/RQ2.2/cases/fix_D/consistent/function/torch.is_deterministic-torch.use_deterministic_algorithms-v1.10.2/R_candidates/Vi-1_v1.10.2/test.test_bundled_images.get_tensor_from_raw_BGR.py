def get_tensor_from_raw_BGR(im) -> torch.Tensor:
    raw_data = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    raw_data = torch.from_numpy(raw_data).float()
    raw_data = raw_data.permute(2, 0, 1)
    raw_data = torch.div(raw_data, 255).unsqueeze(0)
    return raw_data
