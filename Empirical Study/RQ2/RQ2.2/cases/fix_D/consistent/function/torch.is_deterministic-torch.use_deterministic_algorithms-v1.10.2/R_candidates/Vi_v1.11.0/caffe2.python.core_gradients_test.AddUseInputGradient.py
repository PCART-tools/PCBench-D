@GradientRegistry.RegisterGradient('UseInput')
def AddUseInputGradient(op, g_output):
    return (
        CopyDeviceOption(
            CreateOperator(
                'UseInputGradient',
                list(op.input) + NeedAll(op, g_output), GIS(op)),
            op),
        GIS(op)
    )
