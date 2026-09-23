def _no_mutation(self, *args, **kwargs):
    raise NotImplementedError(f"'{type(self).__name__}' object does not support mutation. {_help_mutation}")
