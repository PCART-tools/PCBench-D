    @doc(klass=_shared_doc_kwargs["klass"])
    def ffill(
        self: NDFrameT,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> NDFrameT | None:
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='ffill'``.

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.
        """
        return self.fillna(
            method="ffill", axis=axis, inplace=inplace, limit=limit, downcast=downcast
        )
