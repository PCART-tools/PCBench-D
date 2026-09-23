def runOpOnInput(
    device_option,
    op,
    inputs,
    input_device_options=None,
):
    op = copy.deepcopy(op)
    op.device_option.CopyFrom(device_option)

    with temp_workspace():
        if (len(op.input) > len(inputs)):
            raise ValueError(
                'must supply an input for each input on the op: %s vs %s' %
                (op.input, inputs))
        _input_device_options = input_device_options or \
            core.InferOpBlobDevicesAsDict(op)[0]
        for (n, b) in zip(op.input, inputs):
            workspace.FeedBlob(
                n,
                b,
                device_option=_input_device_options.get(n, device_option)
            )
        workspace.RunOperatorOnce(op)
        outputs_to_check = list(range(len(op.output)))
        outs = []
        for output_index in outputs_to_check:
            output_blob_name = op.output[output_index]
            output = workspace.FetchBlob(output_blob_name)
            outs.append(output)
        return outs
