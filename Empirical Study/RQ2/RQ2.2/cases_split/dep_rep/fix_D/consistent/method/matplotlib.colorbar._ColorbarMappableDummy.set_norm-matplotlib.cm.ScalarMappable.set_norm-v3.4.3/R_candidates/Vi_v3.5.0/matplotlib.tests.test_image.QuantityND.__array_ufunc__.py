    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        func = getattr(ufunc, method)
        if "out" in kwargs:
            raise NotImplementedError
        if len(inputs) == 1:
            i0 = inputs[0]
            unit = getattr(i0, "units", "dimensionless")
            out_arr = func(np.asarray(i0), **kwargs)
        elif len(inputs) == 2:
            i0 = inputs[0]
            i1 = inputs[1]
            u0 = getattr(i0, "units", "dimensionless")
            u1 = getattr(i1, "units", "dimensionless")
            u0 = u1 if u0 is None else u0
            u1 = u0 if u1 is None else u1
            if ufunc in [np.add, np.subtract]:
                if u0 != u1:
                    raise ValueError
                unit = u0
            elif ufunc == np.multiply:
                unit = f"{u0}*{u1}"
            elif ufunc == np.divide:
                unit = f"{u0}/({u1})"
            else:
                raise NotImplementedError
            out_arr = func(i0.view(np.ndarray), i1.view(np.ndarray), **kwargs)
        else:
            raise NotImplementedError
        if unit is None:
            out_arr = np.array(out_arr)
        else:
            out_arr = QuantityND(out_arr, unit)
        return out_arr
