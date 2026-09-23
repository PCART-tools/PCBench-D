def FillRandomNetworkInputs(net, input_dims, input_types):
    C.fill_random_network_inputs(net.Proto().SerializeToString(), input_dims, input_types)
