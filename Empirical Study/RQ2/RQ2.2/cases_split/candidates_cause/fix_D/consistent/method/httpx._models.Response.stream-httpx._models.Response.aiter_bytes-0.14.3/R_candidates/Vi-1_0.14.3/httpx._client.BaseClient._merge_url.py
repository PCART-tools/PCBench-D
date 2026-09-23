    def _merge_url(self, url: URLTypes) -> URL:
        """
        Merge a URL argument together with any 'base_url' on the client,
        to create the URL used for the outgoing request.
        """
        merge_url = URL(url)
        if merge_url.is_relative_url:
            # We always ensure the base_url paths include the trailing '/',
            # and always strip any leading '/' from the merge URL.
            merge_url = merge_url.copy_with(path=merge_url.path.lstrip("/"))
            return self.base_url.join(merge_url)
        return merge_url
