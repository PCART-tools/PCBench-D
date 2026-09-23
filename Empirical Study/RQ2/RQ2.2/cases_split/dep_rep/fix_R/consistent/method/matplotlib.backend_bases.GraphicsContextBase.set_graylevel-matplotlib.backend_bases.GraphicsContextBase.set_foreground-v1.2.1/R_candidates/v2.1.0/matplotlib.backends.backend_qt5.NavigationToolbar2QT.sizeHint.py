        def sizeHint(self):
            size = super(NavigationToolbar2QT, self).sizeHint()
            size.setHeight(max(48, size.height()))
            return size
