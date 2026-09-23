    def limit(self, n: int = 5) -> Self:
        """
        Get the first `n` rows.

        Alias for :func:`DataFrame.head`.

        Parameters
        ----------
        n
            Number of rows to return. If a negative value is passed, return all rows
            except the last `abs(n)`.

        See Also
        --------
        head

        """
        return self.head(n)
