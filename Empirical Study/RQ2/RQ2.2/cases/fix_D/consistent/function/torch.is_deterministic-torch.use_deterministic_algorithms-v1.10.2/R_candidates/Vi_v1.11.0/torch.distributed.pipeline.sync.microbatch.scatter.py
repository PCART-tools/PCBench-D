def scatter(*inputs, chunks: int) -> List[Batch]:
    """Splits an input mini-batch into multiple micro-batches."""
    if len(inputs) == 1 and isinstance(inputs[0], Tensor):
        return [Batch(x) for x in inputs[0].chunk(chunks)]

    batches: List[Any] = [[] for _ in range(chunks)]
    # Actual number of chunks produced
    num_chunks = -1
    for input in inputs:
        if torch.is_tensor(input):
            # Chunk only tensors.
            tensors = input.chunk(chunks)

            # Validate number of chunks equal across all inputs.
            if num_chunks != -1 and num_chunks != len(tensors):
                raise RuntimeError(f'Found different number of chunks produced for inputs: {num_chunks} and {len(tensors)}')
            num_chunks = len(tensors)

            for i, tensor in enumerate(tensors):
                batches[i].append(tensor)
        else:
            # Replicate non-tensors or tensors wrapped with 'NoChunk'.
            for i in range(chunks):
                if isinstance(input, NoChunk):
                    # Extract the tensor out.
                    batches[i].append(input.tensor)
                else:
                    batches[i].append(input)

    # Truncate to actual number of chunks
    batches = batches[:num_chunks]

    return [Batch(x) for x in batches]
