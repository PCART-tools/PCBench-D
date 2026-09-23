def chunked_forward(model, input, chunks=CHUNKS):
    output_chunks = []

    for chunk in input.chunk(chunks):
        output_chunks.append(model(chunk))

    return torch.cat(output_chunks)
