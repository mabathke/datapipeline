from airflow.hooks.postgres_hook import PostgresHook

def create_table():
    TABLE_NAME = "chargingstations"
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        betreiber TEXT,
        strasse TEXT,
        hausnummer TEXT,
        adresszusatz TEXT,
        postleitzahl TEXT,
        ort TEXT,
        bundesland TEXT,
        kreis TEXT,
        breitengrad FLOAT,
        laengengrad FLOAT,
        inbetriebnahmedatum DATE,
        nennleistung_ladeeinrichtung_kw FLOAT,
        art_der_ladeeinrichtung TEXT,
        anzahl_ladepunkte INT,
        steckertypen1 TEXT,
        p1_kw FLOAT,
        public_key1 TEXT,
        steckertypen2 TEXT,
        p2_kw FLOAT,
        public_key2 TEXT,
        steckertypen3 TEXT,
        p3_kw FLOAT,
        public_key3 TEXT,
        steckertypen4 TEXT,
        p4_kw FLOAT,
        public_key4 TEXT
    );
    """
    pg_hook = PostgresHook(postgres_conn_id="datapipeline_postgres")
    pg_hook.run(create_sql)
