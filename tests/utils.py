import string
import random
from attrdict import AttrDict
import sys
import os.path
basepath = os.path.dirname(__file__) + "/.."
if basepath not in sys.path:
    sys.path.append(basepath)
from app.config.base import port
from app.config.base import hostname


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

staticValues = AttrDict({
    "user_id": 1,
    "user_obj": {},
    "token": "",
    "base_url": "http://" + hostname + ":" + str(port) if port else str(5001),
})
