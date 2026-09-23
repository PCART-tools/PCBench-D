def InferOpBlobDevicesAsDict(op):
    input_dev_list, output_dev_list = InferOpBlobDevices(op)
    input_dict = {
        op.input[i]: input_dev_list[i]
        for i in range(len(op.input))
    }
    output_dict = {
        op.output[i]: output_dev_list[i]
        for i in range(len(op.output))
    }
    return input_dict, output_dict
