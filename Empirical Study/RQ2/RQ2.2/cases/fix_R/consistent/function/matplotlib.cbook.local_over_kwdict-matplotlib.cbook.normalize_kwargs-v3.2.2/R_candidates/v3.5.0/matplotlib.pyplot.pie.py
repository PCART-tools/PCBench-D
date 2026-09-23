@_copy_docstring_and_deprecators(Axes.pie)
def pie(
        x, explode=None, labels=None, colors=None, autopct=None,
        pctdistance=0.6, shadow=False, labeldistance=1.1,
        startangle=0, radius=1, counterclock=True, wedgeprops=None,
        textprops=None, center=(0, 0), frame=False,
        rotatelabels=False, *, normalize=True, data=None):
    return gca().pie(
        x, explode=explode, labels=labels, colors=colors,
        autopct=autopct, pctdistance=pctdistance, shadow=shadow,
        labeldistance=labeldistance, startangle=startangle,
        radius=radius, counterclock=counterclock,
        wedgeprops=wedgeprops, textprops=textprops, center=center,
        frame=frame, rotatelabels=rotatelabels, normalize=normalize,
        **({"data": data} if data is not None else {}))
