    def __init__(self, hatch, density):
        self.num_lines = int((hatch.count('/') + hatch.count('x') +
                          hatch.count('X')) * density)
        if self.num_lines:
            self.num_vertices = (self.num_lines + 1) * 2
        else:
            self.num_vertices = 0
