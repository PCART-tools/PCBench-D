    def _interpolate_single_key(self, return_key, tri_index, x, y):
        if return_key == 'z':
            return (self._plane_coefficients[tri_index, 0]*x +
                    self._plane_coefficients[tri_index, 1]*y +
                    self._plane_coefficients[tri_index, 2])
        elif return_key == 'dzdx':
            return self._plane_coefficients[tri_index, 0]
        elif return_key == 'dzdy':
            return self._plane_coefficients[tri_index, 1]
        else:
            raise ValueError("Invalid return_key: " + return_key)
