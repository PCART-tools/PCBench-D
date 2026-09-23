    @torch_required
    def to(self, device: str) -> "BatchEncoding":
        """
        Send all values to device by calling :obj:`v.to(device)` (PyTorch only).

        Args:
            device (:obj:`str` or :obj:`torch.device`): The device to put the tensors on.

        Returns:
            :class:`~transformers.BatchEncoding`:
            The same instance of :class:`~transformers.BatchEncoding` after modification.
        """
        self.data = {k: v.to(device) for k, v in self.data.items()}
        return self
