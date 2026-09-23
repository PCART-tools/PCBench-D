    def __str__(self):
        return "This method must be defined on the concrete class of " \
               + self.class_instance.__class__.__name__
