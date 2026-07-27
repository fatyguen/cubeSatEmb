import time
import yaml

from twin.system import CubeSat
from twin.logger import setup_logger

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    logger = setup_logger()
    config = load_config()
    satellite = CubeSat(config, logger)

    logger.info("CubeSat digital twin booting up...")

    try:
        while True:
            satellite.update()
            if satellite.mode == "SHUTDOWN":
                logger.info("Battery depleted. Shutting down.")
                break
            time.sleep(config["update_rate_seconds"])
    except KeyboardInterrupt:
        logger.info("Simulation stopped by user.")

if __name__ == "__main__":
    main()