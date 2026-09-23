        def sizeHint(self):
            size = super().sizeHint()
            size.setHeight(max(48, size.height()))
            return size
