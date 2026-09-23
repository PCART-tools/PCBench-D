    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    @doc(klass=_shared_doc_kwargs["klass"])
    def bfill(
        self: NDFrameT,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> NDFrameT | None:
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='bfill'``.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.
        """
        return self.fillna(
            method="bfill", axis=axis, inplace=inplace, limit=limit, downcast=downcast
        )
