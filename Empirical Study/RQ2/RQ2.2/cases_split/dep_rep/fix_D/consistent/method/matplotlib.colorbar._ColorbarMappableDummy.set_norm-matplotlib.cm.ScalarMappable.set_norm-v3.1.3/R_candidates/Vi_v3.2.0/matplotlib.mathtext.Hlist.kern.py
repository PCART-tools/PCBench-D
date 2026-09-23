    def kern(self):
        """
        Insert :class:`Kern` nodes between :class:`Char` nodes to set
        kerning.  The :class:`Char` nodes themselves determine the
        amount of kerning they need (in :meth:`~Char.get_kerning`),
        and this function just creates the linked list in the correct
        way.
        """
        new_children = []
        num_children = len(self.children)
        if num_children:
            for i in range(num_children):
                elem = self.children[i]
                if i < num_children - 1:
                    next = self.children[i + 1]
                else:
                    next = None

                new_children.append(elem)
                kerning_distance = elem.get_kerning(next)
                if kerning_distance != 0.:
                    kern = Kern(kerning_distance)
                    new_children.append(kern)
            self.children = new_children
