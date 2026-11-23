import os
import sys

from db import BASE_DIR, connect

# Children before parents
TABLES_IN_DROP_ORDER = ["Cases", "Reports",
                        "Patients"]

def read_statements(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f.read().splitlines()
                 if not ln.strip().startswith("--")]
    return [s.strip()
            for s in "\n".join(lines).split(";")
            if s.strip()]

def main(reset=False):
    conn = connect()
    with conn:
        with conn.cursor() as cur:
            if reset:
                print("Dropping existing tables...")
                for table in TABLES_IN_DROP_ORDER:
                    cur.execute(f"DROP TABLE IF EXISTS {table}")

            print("Creating tables from schema.sql ...")
            for stmt in read_statements("schema.sql"):
                cur.execute(stmt)

            cur.execute("SELECT COUNT(*) AS n FROM Patients")
            if cur.fetchone()["n"] == 0:
                print("Loading sample data from seed.sql ...")
                for stmt in read_statements("seed.sql"):
                    cur.execute(stmt)
            else:
                print("Patients already exist - "
                    "sample data NOT loaded")
        conn.commit()

if __name__ == "__main__":
    main(reset="--reset" in sys.argv)