    def show_file(self, path, **options):
        """
        Display given file.
        """
        args = ["display"]
        title = options.get("title")
        if title:
            args += ["-title", title]
        args.append(path)

        subprocess.Popen(args)
        return 1
