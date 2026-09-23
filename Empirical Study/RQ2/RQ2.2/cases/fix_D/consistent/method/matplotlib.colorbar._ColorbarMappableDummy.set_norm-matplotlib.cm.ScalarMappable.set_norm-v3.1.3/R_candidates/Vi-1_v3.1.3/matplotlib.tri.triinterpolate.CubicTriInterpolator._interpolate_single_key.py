    def _interpolate_single_key(self, return_key, tri_index, x, y):
        tris_pts = self._tris_pts[tri_index]
        alpha = self._get_alpha_vec(x, y, tris_pts)
        ecc = self._eccs[tri_index]
        dof = np.expand_dims(self._dof[tri_index], axis=1)
        if return_key == 'z':
            return self._ReferenceElement.get_function_values(
                alpha, ecc, dof)
        elif return_key in ['dzdx', 'dzdy']:
            J = self._get_jacobian(tris_pts)
            dzdx = self._ReferenceElement.get_function_derivatives(
                alpha, J, ecc, dof)
            if return_key == 'dzdx':
                return dzdx[:, 0, 0]
            else:
                return dzdx[:, 1, 0]
        else:
            raise ValueError("Invalid return_key: " + return_key)
