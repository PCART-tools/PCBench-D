    def get_children(self):
        """return a list of child artists"""
        children = []
        children.extend(self.collections)
        children.extend(self.patches)
        children.extend(self.lines)
        children.extend(self.texts)
        children.extend(self.artists)
        children.extend(six.itervalues(self.spines))
        children.append(self.xaxis)
        children.append(self.yaxis)
        children.append(self.title)
        children.append(self._left_title)
        children.append(self._right_title)
        children.extend(self.tables)
        children.extend(self.images)
        if self.legend_ is not None:
            children.append(self.legend_)
        children.append(self.patch)
        return children
