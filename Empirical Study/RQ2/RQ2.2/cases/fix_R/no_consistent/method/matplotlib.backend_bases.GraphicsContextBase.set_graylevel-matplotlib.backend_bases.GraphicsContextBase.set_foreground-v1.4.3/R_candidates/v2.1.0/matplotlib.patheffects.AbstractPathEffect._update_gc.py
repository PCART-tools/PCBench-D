    def _update_gc(self, gc, new_gc_dict):
        """
        Update the given GraphicsCollection with the given
        dictionary of properties. The keys in the dictionary are used to
        identify the appropriate set_ method on the gc.

        """
        new_gc_dict = new_gc_dict.copy()

        dashes = new_gc_dict.pop("dashes", None)
        if dashes:
            gc.set_dashes(**dashes)

        for k, v in six.iteritems(new_gc_dict):
            set_method = getattr(gc, 'set_' + k, None)
            if not callable(set_method):
                raise AttributeError('Unknown property {0}'.format(k))
            set_method(v)
        return gc
