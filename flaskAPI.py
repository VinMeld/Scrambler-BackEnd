from flask import Flask, request
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
app = Flask(__name__)
DATABASE = "wordsDatabase.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Word(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))

@app.route("/getword")
def get_word():
    if request.args.get('length') is None:
        return ' '.join(map(str,[words.word for words in Word.query.order_by(func.random()).limit(20)]))
    return ' '.join(map(str,[words.word for words in Word.query.order_by(func.random()).limit(int(request.args.get('length')))]))

@app.route("/postword")
def post_word():
    inputWord = request.args.get('word')
    if inputWord is None:
        return 'please add a word to post'
    exists = Word.query.filter_by(word=inputWord).first() is not None
    if exists:
        return 'word already exists'
    elif not inputWord.isalpha():
        return 'word contains non alpha characters'
    elif len(inputWord) > 7 :
        return 'word is too long!'
    db.session.add(Word(inputWord))
    db.session.commit()
    return f"Added new word {inputWord}"

if __name__ == "__main__":
    import bjoern
    bjoern.run(app, "10.0.0.218", 8000)

