class QueryBuilder:

    def __init__(self):
        pass

    def build(self, query):
        """
        Prepare the user's query for retrieval.
        """

        if query is None:
            raise ValueError("Query cannot be None.")

        query = str(query).strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        return query