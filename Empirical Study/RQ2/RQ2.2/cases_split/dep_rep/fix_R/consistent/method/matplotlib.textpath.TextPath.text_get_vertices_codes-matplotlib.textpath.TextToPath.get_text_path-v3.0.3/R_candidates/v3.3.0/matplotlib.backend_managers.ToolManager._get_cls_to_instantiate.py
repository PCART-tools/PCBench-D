    def _get_cls_to_instantiate(self, callback_class):
        # Find the class that corresponds to the tool
        if isinstance(callback_class, str):
            # FIXME: make more complete searching structure
            if callback_class in globals():
                callback_class = globals()[callback_class]
            else:
                mod = 'backend_tools'
                current_module = __import__(mod,
                                            globals(), locals(), [mod], 1)

                callback_class = getattr(current_module, callback_class, False)
        if callable(callback_class):
            return callback_class
        else:
            return None
