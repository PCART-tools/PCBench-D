def getGradientForOp(op):
    return core.GradientRegistry.GetGradientForOp(
        op, [s + '_grad' for s in op.output])
