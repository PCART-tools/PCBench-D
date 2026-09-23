def _RemoveLegacyPad(net, net_params, input_dims):
    legacy_pad_ops = []
    for i in range(len(net.op)):
        op_def = net.op[i]
        if re.match(r'^(Conv|ConvTranspose|MaxPool|AveragePool)(\dD)?$',
                    op_def.type):
            for arg in op_def.arg:
                if arg.name == 'legacy_pad':
                    legacy_pad_ops.append(i)
                    break
    if legacy_pad_ops:
        n, c, h, w = input_dims
        dummy_input = np.random.randn(n, c, h, w).astype(np.float32)
        dim_map = _GetLegacyDims(net, net_params, dummy_input, legacy_pad_ops)

        # Running with the legacy pad argument removed
        # compare the dimensions and adjust pad argument when necessary
        ws = workspace.C.Workspace()

        external_input = net.op[0].input[0]
        ws.create_blob(external_input).feed_blob(dummy_input)
        for param in net_params.protos:
            ws.create_blob(param.name) \
              .feed_blob(utils.Caffe2TensorToNumpyArray(param))

        for i in range(len(net.op)):
            op_def = net.op[i]
            if i in legacy_pad_ops:
                arg_map = {}
                for arg in op_def.arg:
                    arg_map[arg.name] = arg
                pads = _GetLegacyPadArgs(op_def, arg_map)
                # remove legacy pad arg
                for j in range(len(op_def.arg)):
                    arg = op_def.arg[j]
                    if arg.name == 'legacy_pad':
                        del op_def.arg[j]
                        break
                output = op_def.output[0]
                # use a new name to avoid the interference with inplace
                nonlegacy_output = output + '_nonlegacy'
                op_def.output[0] = nonlegacy_output
                ws._run_operator(op_def.SerializeToString())
                blob_nonlegacy = ws.fetch_blob(nonlegacy_output)
                # reset output name
                op_def.output[0] = output

                dim1 = dim_map[i]
                dim2 = blob_nonlegacy.shape
                _AdjustDims(op_def, arg_map, pads, dim1, dim2)

            ws._run_operator(op_def.SerializeToString())
    return net
