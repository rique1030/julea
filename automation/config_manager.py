import os 
import json
from .appconfig import config

default_config = {
    "version": 0.0, 
    "default_browser": "chrome",
}

config_path = os.path.join(config.JULEA_PATH, 'config.json')

def get_config():
    try:
        create_config_if_not_exist()
        load_config()
        return default_config
    except Exception as e:
        print(f"{e}")

def get_default_browser() -> str:
    try:
        config = get_config()
        if config: return config["default_browser"]
        return "edge"
    except Exception as e:
        print(f"{e}")
        return "edge"

def create_config_if_not_exist() -> bool:
    if not os.path.isfile(config_path):
        save_config(default_config)
        return True
    return False

def load_config() -> bool:
    if not os.path.isfile(config_path): return False
    with open(config_path, 'r') as f:
        user_config = json.load(f)
        if is_config_deprecated(user_config):
            new_config = update_config(user_config)
            save_config(new_config)
        else:
            global default_config
            default_config = user_config
    return True

def is_config_deprecated(user_config: dict) -> bool:
    user_version = user_config.get("version", -1)
    default_version = default_config["version"]
    if user_version < default_version: 
        print("Current Version: " + str(default_version))
        print("Stashed Version: " + str(user_version))
        print("User Config out of date")
        print("Updating to latest version")
    return user_version < default_version

def update_config(user_config: dict) -> dict:
    config = deep_update(user_config)
    config["version"] = default_config["version"]
    return config

def deep_update(conf: dict) -> dict:
    for key, value in conf.items():
        default_value = default_config.get(key)
        if isinstance(default_value, dict) and isinstance(value, dict):
            default_config[key] = deep_update(value)
        else:
            default_config[key] = value
    return default_config


def save_config(config_values: dict) -> None:
    with open(config_path, 'w') as f:
        json.dump(config_values, f, indent=3)
