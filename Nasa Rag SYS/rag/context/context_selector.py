# ============================================================
# CONTEXT SELECTOR
# ============================================================

class ContextSelector:

    def __init__(self, top_k=3):
        self.top_k = top_k

    def select(self, reranked_results):
        """
        Select the most relevant results from the
        Cross-Encoder reranked candidates.

        Parameters
        ----------
        reranked_results : list
            Results returned by the Cross-Encoder.

        Returns
        -------
        list
            Selected context results.
        """

        if not reranked_results:
            return []

        # ----------------------------------------------------
        # Take the highest-ranked results
        # ----------------------------------------------------

        selected = reranked_results[:self.top_k]

        # ----------------------------------------------------
        # Add final context rank
        # ----------------------------------------------------

        final_results = []

        for rank, result in enumerate(
            selected,
            start=1
        ):

            item = result.copy()

            item["context_rank"] = rank

            final_results.append(item)

        return final_results