    def __getattribute__(self, item):
        # ArrowStringArray and we both inherit from ArrowExtensionArray, which
        # creates inheritance problems (Diamond inheritance)
        if item in ArrowStringArrayMixin.__dict__ and item != "_pa_array":
            return partial(getattr(ArrowStringArrayMixin, item), self)
        return super().__getattribute__(item)
