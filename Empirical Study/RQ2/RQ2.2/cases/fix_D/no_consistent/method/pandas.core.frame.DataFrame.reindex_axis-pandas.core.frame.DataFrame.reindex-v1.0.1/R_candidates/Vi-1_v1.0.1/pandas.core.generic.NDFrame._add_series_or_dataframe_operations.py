    @classmethod
    def _add_series_or_dataframe_operations(cls):
        """
        Add the series or dataframe only operations to the cls; evaluate
        the doc strings again.
        """

        from pandas.core.window import EWM, Expanding, Rolling, Window

        @Appender(Rolling.__doc__)
        def rolling(
            self,
            window,
            min_periods=None,
            center=False,
            win_type=None,
            on=None,
            axis=0,
            closed=None,
        ):
            axis = self._get_axis_number(axis)

            if win_type is not None:
                return Window(
                    self,
                    window=window,
                    min_periods=min_periods,
                    center=center,
                    win_type=win_type,
                    on=on,
                    axis=axis,
                    closed=closed,
                )

            return Rolling(
                self,
                window=window,
                min_periods=min_periods,
                center=center,
                win_type=win_type,
                on=on,
                axis=axis,
                closed=closed,
            )

        cls.rolling = rolling

        @Appender(Expanding.__doc__)
        def expanding(self, min_periods=1, center=False, axis=0):
            axis = self._get_axis_number(axis)
            return Expanding(self, min_periods=min_periods, center=center, axis=axis)

        cls.expanding = expanding

        @Appender(EWM.__doc__)
        def ewm(
            self,
            com=None,
            span=None,
            halflife=None,
            alpha=None,
            min_periods=0,
            adjust=True,
            ignore_na=False,
            axis=0,
        ):
            axis = self._get_axis_number(axis)
            return EWM(
                self,
                com=com,
                span=span,
                halflife=halflife,
                alpha=alpha,
                min_periods=min_periods,
                adjust=adjust,
                ignore_na=ignore_na,
                axis=axis,
            )

        cls.ewm = ewm
