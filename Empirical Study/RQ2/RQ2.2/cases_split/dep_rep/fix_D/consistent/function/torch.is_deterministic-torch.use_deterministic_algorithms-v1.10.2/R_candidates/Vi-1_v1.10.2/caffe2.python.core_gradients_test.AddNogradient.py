@GradientRegistry.RegisterGradient('Nogradient')
def AddNogradient(op, g_output):
    return (
        [],
        [None for s in op.input]
    )
