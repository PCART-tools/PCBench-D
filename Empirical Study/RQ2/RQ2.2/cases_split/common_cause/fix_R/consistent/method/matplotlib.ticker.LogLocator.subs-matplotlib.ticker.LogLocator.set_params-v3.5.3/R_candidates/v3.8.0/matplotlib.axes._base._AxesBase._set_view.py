    def _set_view(self, view):
        """
        Apply a previously saved view.

        This method is called when restoring a view (with the return value of
        :meth:`_get_view` as argument), such as with the navigation buttons.

        Subclasses that override :meth:`_get_view` also need to override this method
        accordingly.
        """
        self.set(**view)
