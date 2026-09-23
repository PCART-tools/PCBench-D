def _broadcast_coalesced_reshape(
    tensors: Sequence[torch.Tensor],
    devices: Sequence[Union[int, torch.device]],
    detach: bool = False,
) -> list[list[torch.Tensor]]:
    from torch.nn.parallel._functions import Broadcast

    if detach:
        return comm.broadcast_coalesced(tensors, devices)
    else:
        # Use the autograd function to broadcast if not detach
        if len(tensors) > 0:
            tensor_copies = Broadcast.apply(devices, *tensors)
            return [
                tensor_copies[i : i + len(tensors)]
                for i in range(0, len(tensor_copies), len(tensors))
            ]
        else:
            return []
