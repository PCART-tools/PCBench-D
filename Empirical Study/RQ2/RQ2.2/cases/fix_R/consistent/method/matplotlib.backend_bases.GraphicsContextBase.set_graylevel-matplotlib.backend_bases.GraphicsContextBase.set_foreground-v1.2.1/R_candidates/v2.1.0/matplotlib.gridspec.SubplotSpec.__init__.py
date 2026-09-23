    def __init__(self, gridspec, num1, num2=None):
        """
        The subplot will occupy the num1-th cell of the given
        gridspec.  If num2 is provided, the subplot will span between
        num1-th cell and num2-th cell.

        The index starts from 0.
        """

        rows, cols = gridspec.get_geometry()
        total = rows * cols

        self._gridspec = gridspec
        self.num1 = num1
        self.num2 = num2
