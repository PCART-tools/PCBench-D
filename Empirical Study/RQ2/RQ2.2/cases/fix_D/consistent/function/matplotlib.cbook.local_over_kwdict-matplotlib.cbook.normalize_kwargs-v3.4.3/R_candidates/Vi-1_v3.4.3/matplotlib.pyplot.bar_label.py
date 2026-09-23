@_copy_docstring_and_deprecators(Axes.bar_label)
def bar_label(
        container, labels=None, *, fmt='%g', label_type='edge',
        padding=0, **kwargs):
    return gca().bar_label(
        container, labels=labels, fmt=fmt, label_type=label_type,
        padding=padding, **kwargs)
