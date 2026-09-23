    @final
    @doc(
        where,
        klass=_shared_doc_kwargs["klass"],
        cond="False",
        cond_rev="True",
        name="mask",
        name_other="where",
    )
    def mask(
        self,
        cond,
        other=lib.no_default,
        *,
        inplace: bool_t = False,
        axis: Axis | None = None,
        level: Level | None = None,
    ) -> Self | None:
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            if not PYPY and using_copy_on_write():
                if sys.getrefcount(self) <= REF_COUNT:
                    warnings.warn(
                        _chained_assignment_method_msg,
                        ChainedAssignmentError,
                        stacklevel=2,
                    )

        cond = common.apply_if_callable(cond, self)

        # see gh-21891
        if not hasattr(cond, "__invert__"):
            cond = np.array(cond)

        return self.where(
            ~cond,
            other=other,
            inplace=inplace,
            axis=axis,
            level=level,
        )
