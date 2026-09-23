@_copy_docstring_and_deprecators(Axes.table)
def table(
        cellText=None, cellColours=None, cellLoc='right',
        colWidths=None, rowLabels=None, rowColours=None,
        rowLoc='left', colLabels=None, colColours=None,
        colLoc='center', loc='bottom', bbox=None, edges='closed',
        **kwargs):
    return gca().table(
        cellText=cellText, cellColours=cellColours, cellLoc=cellLoc,
        colWidths=colWidths, rowLabels=rowLabels,
        rowColours=rowColours, rowLoc=rowLoc, colLabels=colLabels,
        colColours=colColours, colLoc=colLoc, loc=loc, bbox=bbox,
        edges=edges, **kwargs)
