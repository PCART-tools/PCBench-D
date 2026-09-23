@GradientRegistry.RegisterGradient('UseOutput')
def AddUseOutputGradient(op, g_output):
    return (
        CopyDeviceOption(
            CreateOperator(
                'UseOutputGradient',
                list(op.output) + NeedAll(op, g_output), GIS(op)),
            op),
        GIS(op)
    )
