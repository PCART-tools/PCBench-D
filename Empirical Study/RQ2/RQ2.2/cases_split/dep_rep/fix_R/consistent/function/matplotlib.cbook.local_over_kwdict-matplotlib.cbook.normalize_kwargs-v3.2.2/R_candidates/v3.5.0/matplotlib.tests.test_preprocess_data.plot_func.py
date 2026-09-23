@_preprocess_data(replace_names=["x", "y"], label_namer="y")
def plot_func(ax, x, y, ls="x", label=None, w="xyz"):
    return ("x: %s, y: %s, ls: %s, w: %s, label: %s" % (
        list(x), list(y), ls, w, label))
