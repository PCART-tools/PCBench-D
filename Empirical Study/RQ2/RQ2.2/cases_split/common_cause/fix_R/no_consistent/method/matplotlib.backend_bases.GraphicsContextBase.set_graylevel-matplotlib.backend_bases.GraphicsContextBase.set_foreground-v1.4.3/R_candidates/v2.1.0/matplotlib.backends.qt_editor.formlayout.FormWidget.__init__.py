    def __init__(self, data, comment="", parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.data = copy.deepcopy(data)
        self.widgets = []
        self.formlayout = QtWidgets.QFormLayout(self)
        if comment:
            self.formlayout.addRow(QtWidgets.QLabel(comment))
            self.formlayout.addRow(QtWidgets.QLabel(" "))
        if DEBUG:
            print("\n"+("*"*80))
            print("DATA:", self.data)
            print("*"*80)
            print("COMMENT:", comment)
            print("*"*80)
