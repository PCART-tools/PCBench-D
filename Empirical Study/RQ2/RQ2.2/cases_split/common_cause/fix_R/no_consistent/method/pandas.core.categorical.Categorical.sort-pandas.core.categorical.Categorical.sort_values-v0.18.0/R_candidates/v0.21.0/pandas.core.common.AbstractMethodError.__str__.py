    def __str__(self):
        msg = "This method must be defined in the concrete class of {name}"
        return (msg.format(name=self.class_instance.__class__.__name__))
