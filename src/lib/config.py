import yaml

from model.config import Config


def load_config(config_file: str) -> Config:
    with open(config_file, 'r') as file:
        config_data = yaml.safe_load(file)
    return Config(**config_data)


config = load_config('./config/settings.yaml')
