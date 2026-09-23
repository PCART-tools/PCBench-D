    def _get_op_result_fill_value(self, other, func):
        own_default = self.default_fill_value

        if isinstance(other, DataFrame):
            # i.e. called from _combine_frame

            other_default = getattr(other, 'default_fill_value', np.nan)

            # if the fill values are the same use them? or use a valid one
            if own_default == other_default:
                # TOOD: won't this evaluate as False if both are np.nan?
                fill_value = own_default
            elif np.isnan(own_default) and not np.isnan(other_default):
                fill_value = other_default
            elif not np.isnan(own_default) and np.isnan(other_default):
                fill_value = own_default
            else:
                fill_value = None

        elif isinstance(other, SparseSeries):
            # i.e. called from _combine_match_index

            # fill_value is a function of our operator
            if isna(other.fill_value) or isna(own_default):
                fill_value = np.nan
            else:
                fill_value = func(np.float64(own_default),
                                  np.float64(other.fill_value))

        else:
            raise NotImplementedError(type(other))

        return fill_value
