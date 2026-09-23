class ReverseManyToOneDescriptor(object):
    """
    Accessor to the related objects manager on the reverse side of a
    many-to-one relation.

    In the example::

        class Child(Model):
            parent = ForeignKey(Parent, related_name='children')

    ``parent.children`` is a ``ReverseManyToOneDescriptor`` instance.

    Most of the implementation is delegated to a dynamically defined manager
    class built by ``create_forward_many_to_many_manager()`` defined below.
    """

    def __init__(self, rel):
        self.rel = rel
        self.field = rel.field

    @cached_property
    def related_manager_cls(self):
        return create_reverse_many_to_one_manager(
            self.rel.related_model._default_manager.__class__,
            self.rel,
        )

    def __get__(self, instance, instance_type=None):
        """
        Get the related objects through the reverse relation.

        With the example above, when getting ``parent.children``:

        - ``self`` is the descriptor managing the ``children`` attribute
        - ``instance`` is the ``parent`` instance
        - ``instance_type`` in the ``Parent`` class (we don't need it)
        """
        if instance is None:
            return self

        return self.related_manager_cls(instance)

    def __set__(self, instance, value):
        """
        Set the related objects through the reverse relation.

        With the example above, when setting ``parent.children = children``:

        - ``self`` is the descriptor managing the ``children`` attribute
        - ``instance`` is the ``parent`` instance
        - ``value`` in the ``children`` sequence on the right of the equal sign
        """
        manager = self.__get__(instance)
        manager.set(value)
