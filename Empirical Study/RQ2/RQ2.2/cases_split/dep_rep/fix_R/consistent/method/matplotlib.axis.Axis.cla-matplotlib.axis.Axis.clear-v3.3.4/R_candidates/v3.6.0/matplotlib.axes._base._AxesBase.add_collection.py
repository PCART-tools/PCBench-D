    def add_collection(self, collection, autolim=True):
        """
        Add a `.Collection` to the Axes; return the collection.
        """
        self._deprecate_noninstance('add_collection', mcoll.Collection,
                                    collection=collection)
        label = collection.get_label()
        if not label:
            collection.set_label(f'_child{len(self._children)}')
        self._children.append(collection)
        collection._remove_method = self._children.remove
        self._set_artist_props(collection)

        if collection.get_clip_path() is None:
            collection.set_clip_path(self.patch)

        if autolim:
            # Make sure viewLim is not stale (mostly to match
            # pre-lazy-autoscale behavior, which is not really better).
            self._unstale_viewLim()
            datalim = collection.get_datalim(self.transData)
            points = datalim.get_points()
            if not np.isinf(datalim.minpos).all():
                # By definition, if minpos (minimum positive value) is set
                # (i.e., non-inf), then min(points) <= minpos <= max(points),
                # and minpos would be superfluous. However, we add minpos to
                # the call so that self.dataLim will update its own minpos.
                # This ensures that log scales see the correct minimum.
                points = np.concatenate([points, [datalim.minpos]])
            self.update_datalim(points)

        self.stale = True
        return collection
