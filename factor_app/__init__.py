from flask import Flask
app = Flask(__name__)

import factor_app.views
import factor_app.factor_service
import factor_app.redis_service