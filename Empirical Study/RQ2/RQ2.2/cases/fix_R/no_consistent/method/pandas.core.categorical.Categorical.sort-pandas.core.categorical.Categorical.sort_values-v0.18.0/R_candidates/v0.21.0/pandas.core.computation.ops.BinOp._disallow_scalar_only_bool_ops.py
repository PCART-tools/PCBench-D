    def _disallow_scalar_only_bool_ops(self):
        if ((self.lhs.isscalar or self.rhs.isscalar) and
            self.op in _bool_ops_dict and
            (not (issubclass(self.rhs.return_type, (bool, np.bool_)) and
                  issubclass(self.lhs.return_type, (bool, np.bool_))))):
            raise NotImplementedError("cannot evaluate scalar only bool ops")
