import sqlite3


class DatabaseRepository:
    def __init__(self) -> None:
        self.database = "../../data/arxiv_curator.db"
        self.connection = sqlite3.connect(self.database)

    def get_existing_dois(self) -> set[str]:
        doi_set = set()

        cursor = self.connection.cursor()
        arxiv_ids = cursor.execute("""SELECT arxiv_id FROM papers""")

        for id in arxiv_ids:
            doi_set.add(id[0])

        return doi_set
