from myapp import create_app
from flask_cors import CORS
app = create_app()

print("SECRET_KEY is:", app.config["SECRET_KEY"])

# CORS(app, supports_credentials=true,origins)