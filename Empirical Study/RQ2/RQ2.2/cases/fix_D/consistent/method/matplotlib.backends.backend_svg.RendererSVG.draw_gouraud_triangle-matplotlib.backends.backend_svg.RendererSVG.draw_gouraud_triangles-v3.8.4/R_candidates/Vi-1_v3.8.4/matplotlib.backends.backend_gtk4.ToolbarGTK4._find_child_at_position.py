    def _find_child_at_position(self, group, position):
        children = [None]
        child = self._groups[group].get_first_child()
        while child is not None:
            children.append(child)
            child = child.get_next_sibling()
        return children[position]
