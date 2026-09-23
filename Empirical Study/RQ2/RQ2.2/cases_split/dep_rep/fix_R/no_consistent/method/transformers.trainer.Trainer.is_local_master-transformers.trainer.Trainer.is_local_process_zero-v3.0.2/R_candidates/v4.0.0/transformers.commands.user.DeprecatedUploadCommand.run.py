    def run(self):
        print(
            ANSI.red(
                "Deprecated: used to be the way to upload a model to S3."
                " We now use a git-based system for storing models and other artifacts."
                " Use the `repo create` command instead."
            )
        )
        exit(1)
