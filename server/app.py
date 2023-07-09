from flask import Flask, request, session, jsonify, make_response
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.json.compact = False
app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)
db.init_app(app)

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    session['page_views'] = session.get('page_views', 0) + 1
    
    if session['page_views'] <= 3:
        article= Article.query.filter_by(id=id).first()
        article_dict = article.to_dict()
        return make_response(jsonify(article_dict),200)
    else:
        return (jsonify({'message':'Maximum pageview limit reached'}),401)
    
@app.route('/clear', methods=['POST'])
def clear_session():
    session.clear()
    return jsonify({'message': 'Session cleared'})
        
if __name__ == '__main__':
    app.run(port=5555)
    