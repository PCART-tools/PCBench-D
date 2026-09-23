def _wait(batch: Batch, prev_stream: AbstractStream, next_stream: AbstractStream) -> None:
    batch[:] = Wait.apply(prev_stream, next_stream, *batch)
    # Gradients are only supported for float Tensors.
    batch[:] = tuple([x.detach() if torch.is_tensor(x) and not x.is_floating_point() else x for x in batch])
