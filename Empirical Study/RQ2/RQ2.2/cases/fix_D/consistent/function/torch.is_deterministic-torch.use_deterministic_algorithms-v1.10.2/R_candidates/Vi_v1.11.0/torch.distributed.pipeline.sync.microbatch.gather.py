def gather(outputs: List[Batch]):
    """Concatenates output micro-batches into a mini-batch."""
    output: Any

    if outputs[0].atomic:
        tensors = tuple(b.tensor for b in outputs)
        output = torch.cat(tensors)
    else:
        output_buf: List[Any] = []
        for i in range(len(outputs[0])):
            output_type = type(outputs[0][i])
            current_outputs = []
            for batch in outputs:
                if output_type != type(batch[i]):
                    raise TypeError(f'Types for microbatch outputs do not match, found: {output_type} and {type(batch[i])}')
                current_outputs.append(batch[i])

            if torch.is_tensor(outputs[0][i]):
                output_buf.append(torch.cat(current_outputs))
            else:
                output_buf.append(current_outputs)

        output = tuple(output_buf)

    return output
