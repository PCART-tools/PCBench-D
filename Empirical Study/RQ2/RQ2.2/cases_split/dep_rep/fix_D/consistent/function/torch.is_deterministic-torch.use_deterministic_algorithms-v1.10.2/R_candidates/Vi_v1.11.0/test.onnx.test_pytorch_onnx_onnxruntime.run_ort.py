def run_ort(ort_sess, input):
    input = flatten_tuples(input)
    input = to_numpy(input)
    ort_inputs = dict((ort_sess.get_inputs()[i].name, input) for i, input in enumerate(input))
    ort_outs = ort_sess.run(None, ort_inputs)
    return inline_flatten_list(ort_outs, [])
