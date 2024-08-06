import pandas as pd
import sqlalchemy

def copy_data(db_config:dict)->bool:
    src_db_config:dict = db_config['src_db']
    dest_db_config:dict = db_config['dest_db'] 
    table_list:dict = db_config['table_list']
    global_filter:str = db_config['global_filter']
    # Create connections to the source and destination databases
    src_db_conn = sqlalchemy.create_engine(src_db_config['conn_str'])
    dest_db_conn = sqlalchemy.create_engine(dest_db_config['conn_str'])

    table_id = 0
    for table_name in table_list:
        # Specify the table you want to copy
        query = f'''SELECT * FROM [dbo].[{table_name}] {global_filter if table_list[table_name] else ""}'''
        df = pd.read_sql(query, src_db_conn)

        # Write the data to the destination table
        df.to_sql(table_name, dest_db_conn, schema='dbo', index=False, if_exists='replace')

        print(f'({table_id}) [{table_name}] copied.')
        table_id += 1