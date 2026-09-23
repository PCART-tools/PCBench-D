    def show_file(self, path, **options):
        """
        Display given file.
        """
        subprocess.call(["open", "-a", "Preview.app", path])
        executable = sys.executable or shutil.which("python3")
        if executable:
            subprocess.Popen(
                [
                    executable,
                    "-c",
                    "import os, sys, time; time.sleep(20); os.remove(sys.argv[1])",
                    path,
                ]
            )
        return 1
