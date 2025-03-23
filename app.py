from flask import Flask, render_template
from routes.upload import upload_blueprint

app = Flask(__name__)

# Register Blueprints (for modularity)
app.register_blueprint(upload_blueprint, url_prefix="/upload")

@app.route('/')
def home():
    return "Welcome to E-Commerce Sales Data Analyzer!"

if __name__ == '__main__':
    app.run(debug=True)
