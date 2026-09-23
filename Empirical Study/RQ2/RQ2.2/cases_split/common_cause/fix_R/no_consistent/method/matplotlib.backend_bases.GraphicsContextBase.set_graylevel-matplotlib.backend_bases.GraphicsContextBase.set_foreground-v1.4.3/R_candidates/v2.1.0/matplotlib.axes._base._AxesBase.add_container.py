    def add_container(self, container):
        """
        Add a :class:`~matplotlib.container.Container` instance
        to the axes.

        Returns the collection.
        """
        label = container.get_label()
        if not label:
            container.set_label('_container%d' % len(self.containers))
        self.containers.append(container)
        container.set_remove_method(lambda h: self.containers.remove(h))
        return container
