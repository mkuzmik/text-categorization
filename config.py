import os
from instance.dev.development import DevConfig
from instance.prod.production import ProdConfig

DEV_CONFIG = DevConfig()
PROD_CONFIG = ProdConfig()
CONFIG = DEV_CONFIG if os.environ['ENV'] == 'development' else PROD_CONFIG
