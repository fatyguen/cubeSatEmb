import yaml

from twin.system import CubeSat
from twin.logger import setup_logger
from dashboard.dashboard import run_dashboard

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    logger = setup_logger(console_output=False)
    config = load_config()
    satellite = CubeSat(config, logger)

    run_dashboard(
        satellite,
        update_fn=satellite.update,
        tick_delay=config["update_rate_seconds"]
    )

if __name__ == "__main__":
    main()