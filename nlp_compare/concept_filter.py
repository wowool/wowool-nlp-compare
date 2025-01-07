class ConceptFilter:
    def __init__(self, filter_table):
        self.filter_table = filter_table
        self.cmp_all = "all" in filter_table

    def __call__(self, uri):
        if self.cmp_all:
            if uri == "Sentence":
                return False
            return True
        return uri in self.filter_table
