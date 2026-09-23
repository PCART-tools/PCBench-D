    def _resolve_name(self):
        res = self.env.resolve(self.local_name, is_local=self.is_local)
        self.update(res)

        if hasattr(res, "ndim") and res.ndim > 2:
            raise NotImplementedError(
                "N-dimensional objects, where N > 2," " are not supported with eval"
            )
        return res
