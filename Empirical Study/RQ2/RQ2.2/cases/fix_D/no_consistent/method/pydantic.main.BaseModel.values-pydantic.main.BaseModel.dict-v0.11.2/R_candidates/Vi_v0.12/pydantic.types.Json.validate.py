    @classmethod
    def validate(cls, v: str):
        try:
            return json.loads(v)
        except ValueError:
            raise errors.JsonError()
        except TypeError:
            raise errors.JsonTypeError()
