def CreateOperator(
    operator_type,
    inputs,
    outputs,
    name='',
    control_input=None,
    device_option=None,
    arg=None,
    engine=None,
    debug_info=None,
    **kwargs
):
    """A function wrapper that allows one to create operators based on the
    operator type. The type should be a string corresponding to an operator
    registered with Caffe2.
    """
    operator = caffe2_pb2.OperatorDef()
    if (os.environ.get('CAFFE2_DEBUG')):
        stack = traceback.format_stack()
        operator.debug_info = "".join(stack[:-1])

    operator.type = operator_type
    operator.name = name
    # Add rectified inputs and outputs
    inputs = _RectifyInputOutput(inputs)
    outputs = _RectifyInputOutput(outputs)
    operator.input.extend([text_type(i) for i in inputs])
    operator.output.extend([text_type(o) for o in outputs])
    if control_input:
        control_input = _RectifyInputOutput(control_input)
        operator.control_input.extend([text_type(i) for i in control_input])
    # Set device option:
    # (1) If device_option is explicitly set, use device_option.
    # (2) If not, but scope.CurrentDeviceScope() is set,
    #     then we use scope.CurrentDeviceScope().
    # (3) Otherwise, do not set device option.
    if device_option is not None:
        operator.device_option.CopyFrom(device_option)
    elif scope.CurrentDeviceScope() is not None:
        operator.device_option.CopyFrom(scope.CurrentDeviceScope())
    if engine is not None:
        operator.engine = engine
    if debug_info is not None:
        operator.debug_info = debug_info
    # random seed is defined in the device option, so we need to do special
    # care.

    if 'random_seed' in kwargs:
        operator.device_option.random_seed = kwargs['random_seed']
        del kwargs['random_seed']
    # Add given arguments that do not need parsing
    if arg is not None:
        operator.arg.extend(arg)
    # Add all other arguments
    for key, value in viewitems(kwargs):
        if value is not None:
            operator.arg.add().CopyFrom(utils.MakeArgument(key, value))

    if workspace.IsImmediate():
        workspace.RunOperatorImmediate(operator)
    return operator
