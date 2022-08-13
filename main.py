import logging
import stackhttp as stack
from libs import utils
import pyding

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    utils.load_routes()
    http = stack.HTTP("127.0.0.1", 8000)
    http.spin_up()
