@_copy_docstring_and_deprecators(Figure.subplots_adjust)
def subplots_adjust(
        left=None, bottom=None, right=None, top=None, wspace=None,
        hspace=None):
    return gcf().subplots_adjust(
        left=left, bottom=bottom, right=right, top=top, wspace=wspace,
        hspace=hspace)
