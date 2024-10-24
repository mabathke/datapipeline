from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd
from io import StringIO
import requests

CSV_URL = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister.csv"

def download_csv_data():
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        data = StringIO(response.text)
        df = pd.read_csv(data, sep=";", skiprows=9, header=1)
        
        # Rename columns to lowercase and map the CSV columns to table schema
        df = df.rename(columns={
            "Straße": "strasse", 
            "Kreis/kreisfreie Stadt": "kreis", 
            "Längengrad": "laengengrad",
            "Nennleistung Ladeeinrichtung [kW]": "nennleistung_ladeeinrichtung_kw",
            "Art der Ladeeinrichung": "art_der_ladeeinrichtung",
            "P1 [kW]": "p1_kw",
            "P2 [kW]": "p2_kw",
            "P3 [kW]": "p3_kw",
            "P4 [kW]": "p4_kw"
        })

        # Ensure all column names are lowercase
        df.columns = df.columns.str.lower()

        # Convert relevant columns to proper formats
        df['postleitzahl'] = df['postleitzahl'].apply(lambda x: str(x).replace(',', '.').rstrip('.')).astype(float)
        df['breitengrad'] = df['breitengrad'].apply(lambda x: str(x).replace(',', '.').rstrip('.')).astype(float)
        df['laengengrad'] = df['laengengrad'].apply(lambda x: str(x).replace(',', '.').rstrip('.')).astype(float)

        # Convert 'inbetriebnahmedatum' to proper date format YYYY-MM-DD
        df['inbetriebnahmedatum'] = pd.to_datetime(df['inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce')

        # Fix decimal separator for power and numeric columns
        numeric_columns = ['nennleistung_ladeeinrichtung_kw', 'p1_kw', 'p2_kw', 'p3_kw', 'p4_kw']
        for col in numeric_columns:
            df[col] = df[col].apply(lambda x: str(x).replace(',', '.') if pd.notnull(x) else None).astype(float)

        return df
    else:
        raise Exception(f"Failed to download CSV: {response.status_code}")

def insert_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id="datapipeline_postgres")
    engine = pg_hook.get_sqlalchemy_engine()
    
    df = download_csv_data()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    expected_columns = [
        'betreiber', 'strasse', 'hausnummer', 'adresszusatz', 'postleitzahl', 'ort', 'bundesland', 'kreis',
        'breitengrad', 'laengengrad', 'inbetriebnahmedatum', 'nennleistung_ladeeinrichtung_kw', 'art_der_ladeeinrichtung',
        'anzahl_ladepunkte', 'steckertypen1', 'p1_kw', 'public_key1', 'steckertypen2', 'p2_kw', 'public_key2',
        'steckertypen3', 'p3_kw', 'public_key3', 'steckertypen4', 'p4_kw', 'public_key4'
    ]
    
    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
       # Remove duplicate rows based on relevant columns (adjust as necessary)
    df = df.drop_duplicates(subset=['betreiber', 'strasse', 'hausnummer', 'postleitzahl', 'ort'])
    
    df.to_sql("chargingstations", con=engine, if_exists="append", index=False)