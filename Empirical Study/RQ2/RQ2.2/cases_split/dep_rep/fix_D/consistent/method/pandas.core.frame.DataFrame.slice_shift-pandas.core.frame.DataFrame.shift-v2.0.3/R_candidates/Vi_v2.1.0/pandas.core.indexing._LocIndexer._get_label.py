    def _get_label(self, label, axis: AxisInt):
        # GH#5567 this will fail if the label is not present in the axis.
        return self.obj.xs(label, axis=axis)
