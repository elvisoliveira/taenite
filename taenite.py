import os
import sys

try:
    from loguru import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("taenite")

from src.config import BuildConfig
from src.docker_manager import DockerManager


def _print_callback(message):
    print(message)


if __name__ == "__main__":
    config_path = os.path.abspath("config.yaml")
    if not os.path.exists(config_path):
        print("ERROR: config.yaml file not found in current directory")
        sys.exit(1)

    config = BuildConfig.from_yaml_file(config_path)
    manager = DockerManager()
    ok = manager.start_build(config, _print_callback, output_dir=".")
    sys.exit(0 if ok else 1)
