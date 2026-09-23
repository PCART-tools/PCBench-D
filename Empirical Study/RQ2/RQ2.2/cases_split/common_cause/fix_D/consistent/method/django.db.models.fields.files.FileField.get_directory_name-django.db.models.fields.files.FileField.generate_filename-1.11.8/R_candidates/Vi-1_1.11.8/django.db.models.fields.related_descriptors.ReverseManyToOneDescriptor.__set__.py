    def __set__(self, instance, value):
        """
        Set the related objects through the reverse relation.

        With the example above, when setting ``parent.children = children``:

        - ``self`` is the descriptor managing the ``children`` attribute
        - ``instance`` is the ``parent`` instance
        - ``value`` is the ``children`` sequence on the right of the equal sign
        """
        warnings.warn(
            'Direct assignment to the %s is deprecated due to the implicit '
            'save() that happens. Use %s.set() instead.' % self._get_set_deprecation_msg_params(),
            RemovedInDjango20Warning, stacklevel=2,
        )
        manager = self.__get__(instance)
        manager.set(value)
