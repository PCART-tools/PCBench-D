    def __repr__(self):
        args = (self.name, self.left.value(), self.bottom.value(),
                self.right.value(), self.top.value())
        return ('LayoutBox: %25s, (left: %1.3f) (bot: %1.3f) '
               '(right: %1.3f)  (top: %1.3f) ') % args
