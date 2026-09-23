    def show_file(self, path: str, **options: Any) -> int:
        """
        Display given file.
        """
        args = ["xv"]
        title = options.get("title")
        if title:
            args += ["-name", title]
        args.append(path)

        subprocess.Popen(args)
        return 1
