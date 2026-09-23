    @staticmethod
    def default_units(data, axis):
        # the conversion call stack is:
        # default_units->axis_info->convert
        if axis.unit_data is None:
            axis.unit_data = UnitData(data)
        else:
            axis.unit_data.update(data)
        return None
