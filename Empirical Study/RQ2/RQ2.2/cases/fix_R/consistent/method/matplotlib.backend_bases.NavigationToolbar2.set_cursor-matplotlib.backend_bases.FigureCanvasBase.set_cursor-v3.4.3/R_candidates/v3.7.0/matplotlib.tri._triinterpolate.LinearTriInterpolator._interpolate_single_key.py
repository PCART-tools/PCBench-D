    def _interpolate_single_key(self, return_key, tri_index, x, y):
        _api.check_in_list(['z', 'dzdx', 'dzdy'], return_key=return_key)
        if return_key == 'z':
            return (self._plane_coefficients[tri_index, 0]*x +
                    self._plane_coefficients[tri_index, 1]*y +
                    self._plane_coefficients[tri_index, 2])
        elif return_key == 'dzdx':
            return self._plane_coefficients[tri_index, 0]
        else:  # 'dzdy'
            return self._plane_coefficients[tri_index, 1]
