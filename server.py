from waitress import serve
from app import create_app
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('portfolio_server')

app = create_app()

if __name__ == '__main__':
    logger.info("Serving Sharan Challa Portfolio on http://127.0.0.1:5000")
    serve(app, host='0.0.0.0', port=5000, threads=6)
