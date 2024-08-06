import json
import os
from urllib.parse import quote_plus

CONFIGURATION_FILE_NAME = 'configuration.json'

def get_config()->dict:
    global app_config
    if 'app_config' in globals():
        return app_config
    
    config_file_name = os.path.join(os.getcwd(), CONFIGURATION_FILE_NAME)
    with open(config_file_name, 'r') as config_file:
        app_config = json.load(config_file)

    db_config = app_config['db']
    db_config['src_db']['conn_str'] = get_conn_str(db_config['src_db'])
    db_config['dest_db']['conn_str'] = get_conn_str(db_config['dest_db'])
    db_config['global_filter'] = get_filter_str(db_config)
    if db_config['global_filter'] != '':
        db_config['global_filter'] = f" WHERE {db_config['global_filter']} "

    return app_config
    
def get_conn_str(db_instance_config:dict)->str:
    port:str = '' if db_instance_config['port'] < 0 else f":{db_instance_config['port']}"
    pwd = quote_plus(db_instance_config['pwd'])
    return f"mssql+pyodbc://{db_instance_config['username']}:{pwd}@{db_instance_config['host_addr']}{port}/{db_instance_config['db_name']}{db_instance_config['driver']}"

def get_filter_str(db_config:dict)->str:
    return 'AND'.join(db_config['global_filter_list'])
