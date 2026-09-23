    @property
    def to(self):
        warnings.warn(
            "Usage of ForeignObjectRel.to attribute has been deprecated. "
            "Use the model attribute instead.",
            RemovedInDjango20Warning, 2)
        return self.model
