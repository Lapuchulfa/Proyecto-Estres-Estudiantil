from flask import Flask
from config import Config
from flask import redirect, url_for
from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp
from controllers.core_controller import core_bp

app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = Config.SECRET_KEY
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(core_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
    
    
