    def get_children(self):
        return [child for child in cbook.flatten(self) if child is not None]
