def ExtractPredictorNet(
    net_proto,
    input_blobs,
    output_blobs,
    device=None,
    renames=None,
    disabled_inputs=None,
):
    '''
    Takes a model net for training and returns a net which can be
    used for prediction. For example, all gradient operators and
    input operators are removed.
    @param net_proto protobuf of the net you want to process (net.Proto())
    @param input_blobs list/set of blob names that are the inputs of predictor
    @param output_blobs list/set of blob names that are outputs of predictor
    @param device optional device option that is assigned
    @param renames dictionary of blob name to a new name (optional)
    @param disabled_inputs optional set of blobs that are 'switched off'. This
                will cause branches with those blobs as inputs to be removed
    '''
    predict_net = core.Net(net_proto.name + "_predict")
    predict_proto = predict_net.Proto()

    orig_external_inputs = set(net_proto.external_input)
    orig_external_outputs = set(net_proto.external_output)
    input_blobs = {str(b) for b in input_blobs}
    known_blobs = set(orig_external_inputs).union(input_blobs)
    output_blobs = {str(b) for b in output_blobs}
    external_inputs = set(input_blobs)
    external_outputs = set(output_blobs)

    if renames is None:
        renames = {}

    if disabled_inputs is not None:
        known_blobs = known_blobs - set(disabled_inputs)

    ops = list(net_proto.op)

    # Find the range of ops that we should include
    try:
        first_op_with_input = min(
            [
                j for j in range(len(ops))
                if input_blobs.intersection(ops[j].input) and ops[j].type !=
                'StopGradient'
            ]
        )
    except ValueError:
        raise Exception("No ops with input={}".format(input_blobs))
    try:
        last_op_with_output = max(
            [
                j for j in range(len(ops))
                if output_blobs.intersection(ops[j].output)
            ]
        )
    except ValueError:
        raise Exception("No ops with output={}".format(output_blobs))

    def validate_op(op):
        # Check that the op does not have is_test = 0 set. This is a common
        # pitfall with SpatialBN op, at lest.
        for arg in op.arg:
            if arg.name == "is_test" and arg.i == 0:
                raise Exception(
                    "An operator had is_test=0, did you try to extract a " +
                    "predictor from a train model (instead of test model)?" +
                    " Op was: {}".format(str(op))
                )

    def rename_list(proto_list):
        # proto lists don't support assignments
        new_list = proto_list[:]
        for j, b in enumerate(new_list):
            if b in renames:
                new_list[j] = renames[b]

        del proto_list[:]
        proto_list.extend(new_list)

    # Iterate through the ops and only include those whose inputs
    # we can satisfy.
    for op in ops[first_op_with_input:(last_op_with_output + 1)]:
        if known_blobs.issuperset(op.input):

            # Special handling for recurrent nets
            # TODO: when standard argument type for "nets" is introduced,
            # this can be more general
            if op.type == 'RecurrentNetwork':
                for arg in op.arg:
                    if arg.name == 'backward_step_net':
                        arg.ClearField(str('n'))
                    elif arg.name == 'step_net':
                        for step_op in arg.n.op:
                            rename_list(step_op.input)
                            rename_list(step_op.output)
                            if device is not None:
                                step_op.device_option.device_type = device.device_type
                                step_op.device_option.device_id = device.device_id

                        rename_list(arg.n.external_input)
                        rename_list(arg.n.external_output)

                        # Add additional external inputs
                        external_inputs.update(
                            set(arg.n.external_input).intersection(
                                orig_external_inputs
                            )
                        )

            if device is not None:
                op.device_option.device_type = device.device_type
                op.device_option.device_id = device.device_id
            validate_op(op)
            predict_proto.op.extend([op])
            known_blobs.update(op.output)
            external_inputs.update(
                set(op.input).intersection(orig_external_inputs)
            )
            external_outputs.update(
                set(op.output).intersection(orig_external_outputs)
            )

        else:
            logging.debug(
                "Op {} had unknown inputs: {}".format(
                    op.type, set(op.input).difference(known_blobs)
                )
            )

    # Predictor net's external inputs and outputs include only those
    # that are part of this net.
    predict_proto.external_input.extend(external_inputs)
    predict_proto.external_output.extend(external_outputs)

    rename_list(predict_proto.external_input)
    rename_list(predict_proto.external_output)

    renamed_input_blobs = []
    for b in input_blobs:
        if b in renames:
            renamed_input_blobs.append(renames[b])
        else:
            renamed_input_blobs.append(b)

    for op in predict_proto.op:
        rename_list(op.input)
        rename_list(op.output)

    return predict_net, list(
        set(predict_proto.external_input) - set(renamed_input_blobs)
    )
