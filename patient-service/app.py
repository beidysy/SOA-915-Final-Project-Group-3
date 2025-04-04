from app import create_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    logger.info("✅ Patient service has started.")
    app.run(host="0.0.0.0", port=5001, debug=True)

