import configparser
from dataclasses import dataclass

@dataclass(frozen=True)
class Stripe:
    token: str

def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    stripe_token = config["stripe_config"]

    return Stripe(token=stripe_token["token"])
