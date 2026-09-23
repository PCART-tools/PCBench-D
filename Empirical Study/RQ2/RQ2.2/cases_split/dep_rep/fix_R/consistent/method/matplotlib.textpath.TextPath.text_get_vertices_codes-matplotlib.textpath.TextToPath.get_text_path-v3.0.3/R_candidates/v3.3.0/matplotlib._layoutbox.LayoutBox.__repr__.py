    def __repr__(self):
        return (f'LayoutBox: {self.name:25s}, '
                f'(left: {self.left.value():1.3f}) '
                f'(bot: {self.bottom.value():1.3f}) '
                f'(right: {self.right.value():1.3f}) '
                f'(top: {self.top.value():1.3f})')
