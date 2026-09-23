@_api.deprecated("3.3")
class IndexFormatter(Formatter):
    """
    Format the position x to the nearest i-th label where ``i = int(x + 0.5)``.
    Positions where ``i < 0`` or ``i > len(list)`` have no tick labels.

    Parameters
    ----------
    labels : list
        List of labels.
    """
    def __init__(self, labels):
        self.labels = labels
        self.n = len(labels)

    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position pos.

        The position is ignored and the value is rounded to the nearest
        integer, which is used to look up the label.
        """
        i = int(x + 0.5)
        if i < 0 or i >= self.n:
            return ''
        else:
            return self.labels[i]
