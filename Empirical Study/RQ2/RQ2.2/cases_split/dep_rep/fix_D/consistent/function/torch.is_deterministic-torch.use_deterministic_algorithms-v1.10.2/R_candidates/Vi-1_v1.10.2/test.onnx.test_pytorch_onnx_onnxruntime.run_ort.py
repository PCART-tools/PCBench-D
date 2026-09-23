def run_ort(ort_sess, input):
    input_copy = copy.deepcopy(input)
    input, _ = torch.jit._flatten(input_copy)
    inputs = [to_numpy(inp) for inp in input]

    ort_inputs = dict((ort_sess.get_inputs()[i].name, input) for i, input in enumerate(inputs))
    ort_outs = ort_sess.run(None, ort_inputs)
    return inline_flatten_list(ort_outs, [])
