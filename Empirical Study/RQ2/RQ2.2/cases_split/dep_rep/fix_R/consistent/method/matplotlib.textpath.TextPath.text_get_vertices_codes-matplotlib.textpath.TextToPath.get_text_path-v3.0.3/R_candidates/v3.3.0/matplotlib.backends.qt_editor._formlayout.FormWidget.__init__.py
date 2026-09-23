    def __init__(self, data, comment="", with_margin=False, parent=None):
        """
        Parameters
        ----------
        data : list of (label, value) pairs
            The data to be edited in the form.
        comment : str, optional

        with_margin : bool, default: False
            If False, the form elements reach to the border of the widget.
            This is the desired behavior if the FormWidget is used as a widget
            alongside with other widgets such as a QComboBox, which also do
            not have a margin around them.
            However, a margin can be desired if the FormWidget is the only
            widget within a container, e.g. a tab in a QTabWidget.
        parent : QWidget or None
            The parent widget.
        """
        QtWidgets.QWidget.__init__(self, parent)
        self.data = copy.deepcopy(data)
        self.widgets = []
        self.formlayout = QtWidgets.QFormLayout(self)
        if not with_margin:
            self.formlayout.setContentsMargins(0, 0, 0, 0)
        if comment:
            self.formlayout.addRow(QtWidgets.QLabel(comment))
            self.formlayout.addRow(QtWidgets.QLabel(" "))
