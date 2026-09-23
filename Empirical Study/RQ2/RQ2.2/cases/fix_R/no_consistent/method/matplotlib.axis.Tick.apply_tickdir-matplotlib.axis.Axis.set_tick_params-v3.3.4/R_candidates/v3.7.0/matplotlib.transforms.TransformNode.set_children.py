    def set_children(self, *children):
        """
        Set the children of the transform, to let the invalidation
        system know which transforms can invalidate this transform.
        Should be called from the constructor of any transforms that
        depend on other transforms.
        """
        # Parents are stored as weak references, so that if the
        # parents are destroyed, references from the children won't
        # keep them alive.
        for child in children:
            # Use weak references so this dictionary won't keep obsolete nodes
            # alive; the callback deletes the dictionary entry. This is a
            # performance improvement over using WeakValueDictionary.
            ref = weakref.ref(
                self, lambda _, pop=child._parents.pop, k=id(self): pop(k))
            child._parents[id(self)] = ref
