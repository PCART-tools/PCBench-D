def _save_weight_qparams(self, destination, prefix, keep_vars):
    for attr_name in dir(self):
        if "_weight_qparams" == attr_name and \
           isinstance(getattr(self, attr_name), dict):
            weight_qparams = getattr(self, attr_name)
            destination[prefix + attr_name] = weight_qparams
