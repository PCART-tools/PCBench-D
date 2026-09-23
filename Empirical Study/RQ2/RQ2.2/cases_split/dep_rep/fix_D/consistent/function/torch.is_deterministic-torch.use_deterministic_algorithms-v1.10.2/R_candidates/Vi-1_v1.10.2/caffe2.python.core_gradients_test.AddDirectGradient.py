@GradientRegistry.RegisterGradient('Direct')
def AddDirectGradient(op, g_output):
    return (
        CopyDeviceOption(
            CreateOperator('DirectGradient', NeedAll(op, g_output), GIS(op)),
            op),
        GIS(op)
    )
