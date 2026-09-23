    def remove(self):
        super().remove()
        for coll in self.collections:
            coll.remove()
