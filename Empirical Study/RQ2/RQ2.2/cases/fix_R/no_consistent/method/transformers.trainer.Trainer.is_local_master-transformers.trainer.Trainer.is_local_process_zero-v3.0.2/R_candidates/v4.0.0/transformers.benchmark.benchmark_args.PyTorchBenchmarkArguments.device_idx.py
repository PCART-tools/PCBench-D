    @property
    @torch_required
    def device_idx(self) -> int:
        # TODO(PVP): currently only single GPU is supported
        return torch.cuda.current_device()
