    def _wrap_generic_output(self, result, obj):
        if self.axis == 0:
            new_axes = list(obj.axes)
            new_axes[0] = self.grouper.result_index
        elif self.axis == 1:
            x, y, z = obj.axes
            new_axes = [self.grouper.result_index, z, x]
        else:
            x, y, z = obj.axes
            new_axes = [self.grouper.result_index, y, x]

        result = Panel._from_axes(result, new_axes)

        if self.axis == 1:
            result = result.swapaxes(0, 1).swapaxes(0, 2)
        elif self.axis == 2:
            result = result.swapaxes(0, 2)

        return result
