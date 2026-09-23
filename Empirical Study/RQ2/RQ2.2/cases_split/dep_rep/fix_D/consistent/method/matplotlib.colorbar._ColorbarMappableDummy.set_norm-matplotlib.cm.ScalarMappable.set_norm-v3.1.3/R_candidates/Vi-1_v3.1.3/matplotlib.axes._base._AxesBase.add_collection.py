    def add_collection(self, collection, autolim=True):
        """
        Add a `~.Collection` to the axes' collections; return the collection.
        """
        label = collection.get_label()
        if not label:
            collection.set_label('_collection%d' % len(self.collections))
        self.collections.append(collection)
        collection._remove_method = self.collections.remove
        self._set_artist_props(collection)

        if collection.get_clip_path() is None:
            collection.set_clip_path(self.patch)

        if autolim:
            self.update_datalim(collection.get_datalim(self.transData))

        self.stale = True
        return collection
