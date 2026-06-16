import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--year', default=2021, show_default=True, type=int, help='Year of taxi data to ingest')
@click.option('--month', default=1, show_default=True, type=int, help='Month of taxi data to ingest')
@click.option('--target-table', default='yellow_taxi_data', show_default=True, help='Destination table name')
@click.option('--pg-username', default='root', show_default=True, help='PostgreSQL username')
@click.option('--pg-password', default='root', show_default=True, help='PostgreSQL password')
@click.option('--pg-host', default='localhost', show_default=True, help='PostgreSQL host')
@click.option('--pg-database', default='ny_taxi', show_default=True, help='PostgreSQL database name')
@click.option('--pg-port', default='5432', show_default=True, help='PostgreSQL port')
@click.option('--chunksize', default=100000, show_default=True, type=int, help='Number of rows per chunk')
def run(
    year: int,
    month: int,
    target_table: str,
    pg_username: str,
    pg_password: str,
    pg_host: str,
    pg_database: str,
    pg_port: str,
    chunksize: int,
):
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )


if __name__ == '__main__':
    run()