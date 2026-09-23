    def __init__(self, hatch, density):
        self.num_lines = int((hatch.count('|') + hatch.count('+')) * density)
        self.num_vertices = self.num_lines * 2
