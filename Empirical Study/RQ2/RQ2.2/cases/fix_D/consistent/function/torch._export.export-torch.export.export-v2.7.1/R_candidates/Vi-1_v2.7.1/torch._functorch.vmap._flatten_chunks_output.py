def _flatten_chunks_output(chunks_output_):
    # chunks_output is a list of chunked outputs
    # flatten chunked outputs:
    flat_chunks_output = []
    arg_spec = None
    for output in chunks_output_:
        flat_output, arg_specs = tree_flatten(output)
        flat_chunks_output.append(flat_output)
        if arg_spec is None:
            arg_spec = arg_specs

    # transpose chunk dim and flatten structure
    # flat_output_chunks is flat list of chunks
    flat_output_chunks = list(zip(*flat_chunks_output))
    return flat_output_chunks, arg_spec
