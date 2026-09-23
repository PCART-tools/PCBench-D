    def _unreg_site(self, site):
        if site not in self._sites:
            raise RuntimeError("Site {} is not registered in runner {}"
                               .format(site, self))
        self._sites.remove(site)
