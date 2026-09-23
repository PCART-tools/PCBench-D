    def show_file(self, path: str, **options: Any) -> int:
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
