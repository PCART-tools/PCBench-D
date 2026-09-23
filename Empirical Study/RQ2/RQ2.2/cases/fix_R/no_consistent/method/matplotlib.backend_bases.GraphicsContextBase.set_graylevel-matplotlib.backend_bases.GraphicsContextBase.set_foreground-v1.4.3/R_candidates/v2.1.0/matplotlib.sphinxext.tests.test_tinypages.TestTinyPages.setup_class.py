    @classmethod
    def setup_class(cls):
        cls.page_build = tempfile.mkdtemp()
        try:
            cls.html_dir = pjoin(cls.page_build, 'html')
            cls.doctree_dir = pjoin(cls.page_build, 'doctrees')
            # Build the pages with warnings turned into errors
            cmd = [sys.executable, '-msphinx', '-W', '-b', 'html',
                   '-d', cls.doctree_dir,
                   TINY_PAGES,
                   cls.html_dir]
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(
                    "'{} -msphinx' failed with stdout:\n{}\nstderr:\n{}\n"
                    .format(sys.executable, out, err))
        except Exception as e:
            shutil.rmtree(cls.page_build)
            raise e
