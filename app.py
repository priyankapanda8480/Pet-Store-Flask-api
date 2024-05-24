from flask import Flask
from models import db, Category
from admin.routes import admin_bp
from user.routes import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@localhost/petdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    
    db.create_all()

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
     
