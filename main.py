import sys
import uvicorn
import os
from models import migrate

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'migrate':
            migrate()
        if sys.argv[1] == 'start_api':
            host = '0.0.0.0'
            port = int(os.getenv('API_PORT'))
            uvicorn.run("main_api:app", host=host, port=port, log_level="info")
    except IndexError:
        print('error of argv')
