def GetIndexFromGradientList(g_list, name):
    """A helper function to get the index from a gradient list, None if not
    matching."""
    for i, g in enumerate(g_list):
        if g == name:
            return i
        elif type(g) is GradientSlice:
            if (g.indices == name or g.values == name):
                return i
    return None
