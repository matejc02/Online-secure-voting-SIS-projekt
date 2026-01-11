from flask import Flask
from datetime import timedelta
from models.models import VotingStatus
from extensions import db
from services.user_service import create_admin
from controllers.auth_controller import auth_bp
from controllers.candidates_controller import candidate_bp
from controllers.result_controller import result_bp
from controllers.user_controller import user_bp
from controllers.vote_controller import vote_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjm034jhf0439uf423huj546890z2mf03j406h4v'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config["JWT_SECRET_KEY"] = "hnf9weh809f208h9453207tgzh0f2bg208hj9321hrt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

db.init_app(app)

with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(VotingStatus)).scalar():
        db.session.add(VotingStatus(is_active=False))
        db.session.commit()
    create_admin()

app.register_blueprint(auth_bp)
app.register_blueprint(candidate_bp)
app.register_blueprint(result_bp)
app.register_blueprint(user_bp)
app.register_blueprint(vote_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5002)






