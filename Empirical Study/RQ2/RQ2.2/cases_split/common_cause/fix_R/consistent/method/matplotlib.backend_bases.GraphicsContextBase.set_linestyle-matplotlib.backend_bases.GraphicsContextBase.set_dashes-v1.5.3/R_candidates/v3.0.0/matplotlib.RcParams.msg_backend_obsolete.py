    @property
    @cbook.deprecated("3.0")
    def msg_backend_obsolete(self):
        return ("The {} rcParam was deprecated in version 2.2.  In order to "
                "force the use of a specific Qt binding, either import that "
                "binding first, or set the QT_API environment variable.")
