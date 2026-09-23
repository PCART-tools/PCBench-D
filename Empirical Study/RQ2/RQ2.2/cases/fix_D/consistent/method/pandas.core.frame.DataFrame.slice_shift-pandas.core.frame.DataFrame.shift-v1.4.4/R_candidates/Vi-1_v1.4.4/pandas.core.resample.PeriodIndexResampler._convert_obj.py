    def _convert_obj(self, obj: NDFrameT) -> NDFrameT:
        obj = super()._convert_obj(obj)

        if self._from_selection:
            # see GH 14008, GH 12871
            msg = (
                "Resampling from level= or on= selection "
                "with a PeriodIndex is not currently supported, "
                "use .set_index(...) to explicitly set index"
            )
            raise NotImplementedError(msg)

        if self.loffset is not None:
            # Cannot apply loffset/timedelta to PeriodIndex -> convert to
            # timestamps
            self.kind = "timestamp"

        # convert to timestamp
        if self.kind == "timestamp":
            obj = obj.to_timestamp(how=self.convention)

        return obj
