import os
from sshtunnel import SSHTunnelForwarder
import psycopg2
from airflow.providers.postgres.hooks.postgres import PostgresHook


def transmit_data_through_ssh_tunnel():
    try:
        # SSH Tunnel Configuration
        bastion_host = os.getenv('BASTION_PUBLIC_IP')  # Replace with your bastion host public IP
        bastion_username = 'ec2-user'
        ssh_pkey = os.getenv('SSH_PKEY', '/root/.ssh/coolify_bastion_key')  # Path to your private key
        remote_bind_host = os.getenv('RDS_HOST')
        remote_bind_port = 5432
        local_bind_port = 6000  # Local port for the SSH tunnel

        # RDS Database Credentials
        remote_db_name = 'postgres'
        remote_db_user = 'postgres'
        remote_db_password = os.getenv('RDS_PASSWORD')  # Replace with the actual password

        # Establish SSH Tunnel
        with SSHTunnelForwarder(
                (bastion_host, 22),
                ssh_username=bastion_username,
                ssh_pkey=ssh_pkey,
                remote_bind_address=(remote_bind_host, remote_bind_port),
                local_bind_address=('localhost', local_bind_port)
        ) as tunnel:
            pg_hook = PostgresHook(postgres_conn_id='dag_connection')
            connection = pg_hook.get_conn()
            cursor = connection.cursor()

            # Fetch Rows from Local Table
            cursor.execute("SELECT * FROM etl_perfume;")
            rows = cursor.fetchall()

            # print("Number of rows: " + str(len(rows)))
            # print(rows)

            # Connect to Remote RDS via Tunnel
            remote_conn = psycopg2.connect(
                host='localhost',  # Local end of the SSH tunnel
                port=local_bind_port,
                dbname=remote_db_name,
                user=remote_db_user,
                password=remote_db_password
            )
            remote_cur = remote_conn.cursor()

            # TODO: Determine ON CONFLICT behaviour

            # Insert Data into Remote Table
            insert_query = """
            INSERT INTO etl_perfume (id, link, name, brand, rel_year, rel_decade, notes, chart_categories, 
                    chart_numbers, scent, longevity, sillage, bottle, value_for_money)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            remote_cur.executemany(insert_query, rows)
            remote_conn.commit()

            print("Successfully transferred data to Amazon RDS instance")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
        remote_cur.close()
        remote_conn.close()

        return
