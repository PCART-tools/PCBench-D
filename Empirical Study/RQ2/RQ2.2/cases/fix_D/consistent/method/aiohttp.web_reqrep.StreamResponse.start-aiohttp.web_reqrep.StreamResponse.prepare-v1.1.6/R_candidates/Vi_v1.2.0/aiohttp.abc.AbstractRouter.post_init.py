    def post_init(self, app):
        """Post init stage.

        It's not an abstract method for sake of backward compatibility
        but if router wans to be aware about application it should
        override it.

        """
