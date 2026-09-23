    def __repr__(self):
        str = f'LayoutBox: {self.name:25s} {self.nrows}x{self.ncols},\n'
        for i in range(self.nrows):
            for j in range(self.ncols):
                str += f'{i}, {j}: '\
                       f'L({self.lefts[j].value():1.3f}, ' \
                       f'B{self.bottoms[i].value():1.3f}, ' \
                       f'W{self.widths[j].value():1.3f}, ' \
                       f'H{self.heights[i].value():1.3f}, ' \
                       f'innerW{self.inner_widths[j].value():1.3f}, ' \
                       f'innerH{self.inner_heights[i].value():1.3f}, ' \
                       f'ML{self.margins["left"][j].value():1.3f}, ' \
                       f'MR{self.margins["right"][j].value():1.3f}, \n'
        return str
