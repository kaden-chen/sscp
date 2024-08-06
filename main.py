import json

import config
import copier as cp

if __name__ == '__main__':
    app_config = config.get_config()
    print(json.dumps(app_config, indent=3))

    db_config = app_config['db']
    cp.copy_data(db_config)

