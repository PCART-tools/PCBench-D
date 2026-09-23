@_copy_docstring_and_deprecators(Axes.boxplot)
def boxplot(
        x, notch=None, sym=None, vert=None, whis=None,
        positions=None, widths=None, patch_artist=None,
        bootstrap=None, usermedians=None, conf_intervals=None,
        meanline=None, showmeans=None, showcaps=None, showbox=None,
        showfliers=None, boxprops=None, labels=None, flierprops=None,
        medianprops=None, meanprops=None, capprops=None,
        whiskerprops=None, manage_ticks=True, autorange=False,
        zorder=None, *, data=None):
    return gca().boxplot(
        x, notch=notch, sym=sym, vert=vert, whis=whis,
        positions=positions, widths=widths, patch_artist=patch_artist,
        bootstrap=bootstrap, usermedians=usermedians,
        conf_intervals=conf_intervals, meanline=meanline,
        showmeans=showmeans, showcaps=showcaps, showbox=showbox,
        showfliers=showfliers, boxprops=boxprops, labels=labels,
        flierprops=flierprops, medianprops=medianprops,
        meanprops=meanprops, capprops=capprops,
        whiskerprops=whiskerprops, manage_ticks=manage_ticks,
        autorange=autorange, zorder=zorder,
        **({"data": data} if data is not None else {}))
