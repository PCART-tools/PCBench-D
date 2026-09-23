        def info(self) -> email.message.Message:
            info = email.message.Message()
            for key, value in self.response.headers.multi_items():
                #  Note that setting `info[key]` here is an "append" operation,
                # not a "replace" operation.
                # https://docs.python.org/3/library/email.compat32-message.html#email.message.Message.__setitem__
                info[key] = value
            return info
