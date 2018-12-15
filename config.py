import os
from instance.dev.development import DevConfig
from instance.prod.production import ProdConfig

DEV_CONFIG = DevConfig()
PROD_CONFIG = ProdConfig()
CONFIG = PROD_CONFIG if os.environ.get('ENV', 'development') == 'production' else DEV_CONFIG
