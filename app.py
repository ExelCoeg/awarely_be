from myapp import create_app
from flask_cors import CORS
app = create_app()


CORS(app, supports_credentials=True,origins=["http://127.0.0.1:5500", "https://awarely-black.vercel.app/"])