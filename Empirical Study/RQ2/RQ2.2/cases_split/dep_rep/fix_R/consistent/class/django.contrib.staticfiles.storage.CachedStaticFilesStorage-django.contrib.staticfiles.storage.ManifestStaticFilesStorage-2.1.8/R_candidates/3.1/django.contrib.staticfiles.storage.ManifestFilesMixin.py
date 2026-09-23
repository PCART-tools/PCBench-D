class ManifestFilesMixin(HashedFilesMixin):
    manifest_version = '1.0'  # the manifest format standard
    manifest_name = 'staticfiles.json'
    manifest_strict = True
    keep_intermediate_files = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashed_files = self.load_manifest()

    def read_manifest(self):
        try:
            with self.open(self.manifest_name) as manifest:
                return manifest.read().decode()
        except FileNotFoundError:
            return None

    def load_manifest(self):
        content = self.read_manifest()
        if content is None:
            return {}
        try:
            stored = json.loads(content)
        except json.JSONDecodeError:
            pass
        else:
            version = stored.get('version')
            if version == '1.0':
                return stored.get('paths', {})
        raise ValueError("Couldn't load manifest '%s' (version %s)" %
                         (self.manifest_name, self.manifest_version))

    def post_process(self, *args, **kwargs):
        self.hashed_files = {}
        yield from super().post_process(*args, **kwargs)
        if not kwargs.get('dry_run'):
            self.save_manifest()

    def save_manifest(self):
        payload = {'paths': self.hashed_files, 'version': self.manifest_version}
        if self.exists(self.manifest_name):
            self.delete(self.manifest_name)
        contents = json.dumps(payload).encode()
        self._save(self.manifest_name, ContentFile(contents))

    def stored_name(self, name):
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        hash_key = self.hash_key(clean_name)
        cache_name = self.hashed_files.get(hash_key)
        if cache_name is None:
            if self.manifest_strict:
                raise ValueError("Missing staticfiles manifest entry for '%s'" % clean_name)
            cache_name = self.clean_name(self.hashed_name(name))
        unparsed_name = list(parsed_name)
        unparsed_name[2] = cache_name
        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        if '?#' in name and not unparsed_name[3]:
            unparsed_name[2] += '?'
        return urlunsplit(unparsed_name)
