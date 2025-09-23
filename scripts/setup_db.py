import sqlite3

con = sqlite3.connect("../data/arxiv_curator.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS papers (
        arxiv_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        abstract TEXT NOT NULL,
        authors TEXT,
        published_on TEXT
    )"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arxiv_id TEXT NOT NULL,
        final_score INT,
        expected_impact TEXT,
        summary_data TEXT,
        video_ideas TEXT,
        evaluated_at TEXT,
        FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_ID)
    )"""
)
con.close()
