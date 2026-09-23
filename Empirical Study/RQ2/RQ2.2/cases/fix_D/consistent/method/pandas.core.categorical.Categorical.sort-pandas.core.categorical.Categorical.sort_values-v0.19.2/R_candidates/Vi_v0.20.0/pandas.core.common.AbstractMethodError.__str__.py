    def __str__(self):
        return ("This method must be defined in the concrete class of %s" %
                self.class_instance.__class__.__name__)
