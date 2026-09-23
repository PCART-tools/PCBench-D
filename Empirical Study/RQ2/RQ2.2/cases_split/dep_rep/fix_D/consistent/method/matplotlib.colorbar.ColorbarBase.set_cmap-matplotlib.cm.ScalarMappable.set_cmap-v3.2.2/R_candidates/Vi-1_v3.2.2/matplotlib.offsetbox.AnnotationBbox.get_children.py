    def get_children(self):
        children = [self.offsetbox, self.patch]
        if self.arrow_patch:
            children.append(self.arrow_patch)
        return children
