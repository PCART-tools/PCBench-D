    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            _log.info("Tried to remove child that doesn't belong to parent")
