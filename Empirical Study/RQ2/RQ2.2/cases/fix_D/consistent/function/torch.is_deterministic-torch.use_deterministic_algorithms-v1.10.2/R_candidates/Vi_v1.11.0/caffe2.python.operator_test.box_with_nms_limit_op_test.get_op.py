def get_op(input_len, output_len, args):
    input_names = ['in_scores', 'in_boxes', 'in_batch_splits']
    assert input_len <= len(input_names)
    input_names = input_names[:input_len]

    out_names = ['scores', 'boxes', 'classes', 'batch_splits', 'keeps', 'keeps_size']
    assert output_len <= len(out_names)
    out_names = out_names[:output_len]

    op = core.CreateOperator(
        'BoxWithNMSLimit',
        input_names,
        out_names,
        **args)

    return op
