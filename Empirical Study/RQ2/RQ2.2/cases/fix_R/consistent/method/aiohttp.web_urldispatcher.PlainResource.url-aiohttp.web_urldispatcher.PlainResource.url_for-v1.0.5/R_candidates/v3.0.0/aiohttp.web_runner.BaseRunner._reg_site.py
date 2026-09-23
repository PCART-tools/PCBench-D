    def _reg_site(self, site):
        if site in self._sites:
            raise RuntimeError("Site {} is already registered in runner {}"
                               .format(site, self))
        self._sites.add(site)
