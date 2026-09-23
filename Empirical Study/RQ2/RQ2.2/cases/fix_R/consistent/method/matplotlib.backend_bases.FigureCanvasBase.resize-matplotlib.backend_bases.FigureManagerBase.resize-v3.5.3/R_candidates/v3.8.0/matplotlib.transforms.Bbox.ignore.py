    def ignore(self, value):
        """
        Set whether the existing bounds of the box should be ignored
        by subsequent calls to :meth:`update_from_data_xy`.

        value : bool
            - When ``True``, subsequent calls to `update_from_data_xy` will
              ignore the existing bounds of the `Bbox`.
            - When ``False``, subsequent calls to `update_from_data_xy` will
              include the existing bounds of the `Bbox`.
        """
        self._ignore = value
