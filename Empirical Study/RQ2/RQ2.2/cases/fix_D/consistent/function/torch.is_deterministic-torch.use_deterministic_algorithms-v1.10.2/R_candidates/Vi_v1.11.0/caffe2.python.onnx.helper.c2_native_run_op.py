def c2_native_run_op(op_def, inputs):
    ws = Workspace()
    if isinstance(inputs, dict):
        for key, value in inputs.items():
            ws.FeedBlob(key, value, op_def.device_option)
    else:
        assert(len(op_def.input) == len(inputs))
        for key, value in zip(op_def.input, inputs):
            ws.FeedBlob(key, value, op_def.device_option)

    ws.RunOperatorOnce(op_def)

    output_names = op_def.output
    output_values = [ws.FetchBlob(name) for name in output_names]
    return ws, namedtupledict('Outputs', output_names)(*output_values)
