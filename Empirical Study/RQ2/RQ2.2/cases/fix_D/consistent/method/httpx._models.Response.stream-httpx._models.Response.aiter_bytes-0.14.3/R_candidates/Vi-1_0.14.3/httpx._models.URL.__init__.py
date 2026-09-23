    def __init__(self, url: URLTypes = "", params: QueryParamTypes = None) -> None:
        if isinstance(url, str):
            try:
                self._uri_reference = rfc3986.iri_reference(url).encode()
            except rfc3986.exceptions.InvalidAuthority as exc:
                raise InvalidURL(message=str(exc)) from None

            if self.is_absolute_url:
                # We don't want to normalize relative URLs, since doing so
                # removes any leading `../` portion.
                self._uri_reference = self._uri_reference.normalize()
        else:
            self._uri_reference = url._uri_reference

        # Add any query parameters, merging with any in the URL if needed.
        if params:
            if self._uri_reference.query:
                url_params = QueryParams(self._uri_reference.query)
                url_params.update(params)
                query_string = str(url_params)
            else:
                query_string = str(QueryParams(params))
            self._uri_reference = self._uri_reference.copy_with(query=query_string)
