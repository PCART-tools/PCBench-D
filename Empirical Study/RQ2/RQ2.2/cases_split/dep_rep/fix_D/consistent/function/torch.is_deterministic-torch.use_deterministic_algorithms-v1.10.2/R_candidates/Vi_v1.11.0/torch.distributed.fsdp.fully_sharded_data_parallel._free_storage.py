def _free_storage(data: torch.Tensor) -> None:
    """Free underlying storage of a Tensor."""
    if data.storage().size() > 0:
        # Since we're modifying the Tensor's Storage directly, make sure the Tensor
        # is the sole occupant of the Storage.
        assert (
            data.storage_offset() == 0
        ), "The tensor is not the sole occupant of the storage."
        data.storage().resize_(0)  # type: ignore[attr-defined]
