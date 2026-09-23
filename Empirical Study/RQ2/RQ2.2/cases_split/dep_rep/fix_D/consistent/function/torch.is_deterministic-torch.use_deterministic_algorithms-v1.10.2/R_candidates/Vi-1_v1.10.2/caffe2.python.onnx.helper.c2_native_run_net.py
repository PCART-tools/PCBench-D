def c2_native_run_net(init_net, predict_net, inputs, debug_arg=None):
    ws = Workspace()
    if init_net:
        ws.RunNetOnce(init_net)

    if isinstance(inputs, dict):
        for key, value in inputs.items():
            ws.FeedBlob(key, value, predict_net.device_option)
    else:
        uninitialized = [input_name
                         for input_name in predict_net.external_input
                         if not ws.HasBlob(input_name)]
        if len(uninitialized) == len(inputs):
            for key, value in zip(uninitialized, inputs):
                ws.FeedBlob(key, value, predict_net.device_option)
        else:
            # If everything is initialized,
            # we just initialized the first len(inputs) external_input.
            # Added some extra logging to help debug sporadic sandcastle fails
            if len(inputs) > len(predict_net.external_input):
                print("c2_native_run_net assert. len(inputs)=", len(inputs),
                      "len(predict_net.external_input)=",
                      len(predict_net.external_input))
                print("debug_arg: ", debug_arg)
                print("predict_net ", type(predict_net), ":", predict_net)
                print("inputs ", type(inputs), ":", inputs)
            assert(len(inputs) <= len(predict_net.external_input))
            for i in range(len(inputs)):
                ws.FeedBlob(predict_net.external_input[i], inputs[i],
                            predict_net.device_option)

    ws.RunNetOnce(predict_net)

    output_names = predict_net.external_output
    output_values = [ws.FetchBlob(name) for name in output_names]
    return ws, namedtupledict('Outputs', output_names)(*output_values)
