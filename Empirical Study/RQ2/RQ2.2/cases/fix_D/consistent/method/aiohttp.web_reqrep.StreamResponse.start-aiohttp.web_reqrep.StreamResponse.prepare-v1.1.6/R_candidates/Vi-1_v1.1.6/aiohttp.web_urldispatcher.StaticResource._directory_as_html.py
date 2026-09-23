    def _directory_as_html(self, filepath):
        "returns directory's index as html"
        # sanity check
        assert filepath.is_dir()

        posix_dir_len = len(self._directory.as_posix())

        # remove the beginning of posix path, so it would be relative
        # to our added static path
        relative_path_to_dir = filepath.as_posix()[posix_dir_len:]
        index_of = "Index of /{}".format(relative_path_to_dir)
        head = "<head>\n<title>{}</title>\n</head>".format(index_of)
        h1 = "<h1>{}</h1>".format(index_of)

        index_list = []
        dir_index = filepath.iterdir()
        for _file in sorted(dir_index):
            # show file url as relative to static path
            file_url = _file.as_posix()[posix_dir_len:]

            # if file is a directory, add '/' to the end of the name
            if _file.is_dir():
                file_name = "{}/".format(_file.name)
            else:
                file_name = _file.name

            index_list.append(
                '<li><a href="{url}">{name}</a></li>'.format(url=file_url,
                                                             name=file_name)
            )
        ul = "<ul>\n{}\n</ul>".format('\n'.join(index_list))
        body = "<body>\n{}\n{}\n</body>".format(h1, ul)

        html = "<html>\n{}\n{}\n</html>".format(head, body)

        return html
