from vkapi import config
from vkapi.session import Session

session = Session(config.VK_CONFIG["domain"])  # type: ignore


def exceptions():
    return None
