    def _resolve_name(self):
        local_name = str(self.local_name)
        is_local = self.is_local
        if local_name in self.env.scope and isinstance(
            self.env.scope[local_name], type
        ):
            is_local = False

        res = self.env.resolve(local_name, is_local=is_local)
        self.update(res)

        if hasattr(res, "ndim") and res.ndim > 2:
            raise NotImplementedError(
                "N-dimensional objects, where N > 2, are not supported with eval"
            )
        return res
