@_copy_docstring_and_deprecators(Axes.violinplot)
def violinplot(
        dataset, positions=None, vert=True, widths=0.5,
        showmeans=False, showextrema=True, showmedians=False,
        quantiles=None, points=100, bw_method=None, *, data=None):
    return gca().violinplot(
        dataset, positions=positions, vert=vert, widths=widths,
        showmeans=showmeans, showextrema=showextrema,
        showmedians=showmedians, quantiles=quantiles, points=points,
        bw_method=bw_method,
        **({"data": data} if data is not None else {}))
