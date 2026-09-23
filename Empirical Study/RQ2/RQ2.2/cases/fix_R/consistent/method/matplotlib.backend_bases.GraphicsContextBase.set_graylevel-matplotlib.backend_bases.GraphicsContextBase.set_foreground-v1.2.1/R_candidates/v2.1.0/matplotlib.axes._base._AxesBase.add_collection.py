    def add_collection(self, collection, autolim=True):
        """
        Add a :class:`~matplotlib.collections.Collection` instance
        to the axes.

        Returns the collection.
        """
        label = collection.get_label()
        if not label:
            collection.set_label('_collection%d' % len(self.collections))
        self.collections.append(collection)
        self._set_artist_props(collection)

        if collection.get_clip_path() is None:
            collection.set_clip_path(self.patch)

        if autolim:
            self.update_datalim(collection.get_datalim(self.transData))

        collection._remove_method = lambda h: self.collections.remove(h)
        self.stale = True
        return collection
