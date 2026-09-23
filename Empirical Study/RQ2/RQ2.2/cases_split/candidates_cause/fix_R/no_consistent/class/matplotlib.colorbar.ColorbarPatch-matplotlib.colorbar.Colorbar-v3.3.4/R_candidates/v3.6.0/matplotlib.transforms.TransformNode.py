class TransformNode:
    """
    The base class for anything that participates in the transform tree
    and needs to invalidate its parents or be invalidated.  This includes
    classes that are not really transforms, such as bounding boxes, since some
    transforms depend on bounding boxes to compute their values.
    """

    # Invalidation may affect only the affine part.  If the
    # invalidation was "affine-only", the _invalid member is set to
    # INVALID_AFFINE_ONLY
    INVALID_NON_AFFINE = 1
    INVALID_AFFINE = 2
    INVALID = INVALID_NON_AFFINE | INVALID_AFFINE

    # Some metadata about the transform, used to determine whether an
    # invalidation is affine-only
    is_affine = False
    is_bbox = False

    pass_through = False
    """
    If pass_through is True, all ancestors will always be
    invalidated, even if 'self' is already invalid.
    """

    def __init__(self, shorthand_name=None):
        """
        Parameters
        ----------
        shorthand_name : str
            A string representing the "name" of the transform. The name carries
            no significance other than to improve the readability of
            ``str(transform)`` when DEBUG=True.
        """
        self._parents = {}

        # TransformNodes start out as invalid until their values are
        # computed for the first time.
        self._invalid = 1
        self._shorthand_name = shorthand_name or ''

    if DEBUG:
        def __str__(self):
            # either just return the name of this TransformNode, or its repr
            return self._shorthand_name or repr(self)

    def __getstate__(self):
        # turn the dictionary with weak values into a normal dictionary
        return {**self.__dict__,
                '_parents': {k: v() for k, v in self._parents.items()}}

    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak values
        # The extra lambda is to provide a callback to remove dead
        # weakrefs from the dictionary when garbage collection is done.
        self._parents = {
            k: weakref.ref(v, lambda _, pop=self._parents.pop, k=k: pop(k))
            for k, v in self._parents.items() if v is not None}

    def __copy__(self):
        other = copy.copy(super())
        # If `c = a + b; a1 = copy(a)`, then modifications to `a1` do not
        # propagate back to `c`, i.e. we need to clear the parents of `a1`.
        other._parents = {}
        # If `c = a + b; c1 = copy(c)`, then modifications to `a` also need to
        # be propagated to `c1`.
        for key, val in vars(self).items():
            if isinstance(val, TransformNode) and id(self) in val._parents:
                other.set_children(val)  # val == getattr(other, key)
        return other

    def invalidate(self):
        """
        Invalidate this `TransformNode` and triggers an invalidation of its
        ancestors.  Should be called any time the transform changes.
        """
        value = self.INVALID
        if self.is_affine:
            value = self.INVALID_AFFINE
        return self._invalidate_internal(value, invalidating_node=self)

    def _invalidate_internal(self, value, invalidating_node):
        """
        Called by :meth:`invalidate` and subsequently ascends the transform
        stack calling each TransformNode's _invalidate_internal method.
        """
        # determine if this call will be an extension to the invalidation
        # status. If not, then a shortcut means that we needn't invoke an
        # invalidation up the transform stack as it will already have been
        # invalidated.

        # N.B This makes the invalidation sticky, once a transform has been
        # invalidated as NON_AFFINE, then it will always be invalidated as
        # NON_AFFINE even when triggered with a AFFINE_ONLY invalidation.
        # In most cases this is not a problem (i.e. for interactive panning and
        # zooming) and the only side effect will be on performance.
        status_changed = self._invalid < value

        if self.pass_through or status_changed:
            self._invalid = value

            for parent in list(self._parents.values()):
                # Dereference the weak reference
                parent = parent()
                if parent is not None:
                    parent._invalidate_internal(
                        value=value, invalidating_node=self)

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

    def frozen(self):
        """
        Return a frozen copy of this transform node.  The frozen copy will not
        be updated when its children change.  Useful for storing a previously
        known state of a transform where ``copy.deepcopy()`` might normally be
        used.
        """
        return self
