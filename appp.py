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

@app.route("/getword", methods=['GET'])
def get_word():
    if request.args.get('length') is None:
        return ' '.join(map(str,[words.word for words in Word.query.order_by(func.random()).limit(20)]))
    if int(request.args.get('length')) > 0:
        return ' '.join(map(str,[words.word for words in Word.query.order_by(func.random()).limit(int(request.args.get('length')))]))
    return 'Error'

@app.route("/all", methods=['GET'])
def get_all():
    rows = Word.query.count()
    return ' '.join(map(str,[words.word for words in Word.query.order_by(func.random()).limit(rows)]))

@app.route("/count", methods=['GET'])
def get_count():
    rows = Word.query.count()
    return str(rows)

@app.route("/postword", methods=['GET'])
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
    db.session.add(Word(word = inputWord))
    db.session.commit()
    return f"Added new word {inputWord}"
@app.route("/deleteword", methods=['GET'])
def delete_word():
    inputWord = request.args.get('word')
    if inputWord is None:
        return 'please add a word to delete'
    exists = Word.query.filter_by(word=inputWord).first()
    if exists:
        Word.query.filter_by(word=inputWord).delete()
        db.session.commit()
        return f"deleted {inputWord}"
    else:
        return 'could not find word'


if __name__ == "__main__":
    import bjoern
    bjoern.run(app, "10.0.0.218", 8000)
# def getApp():
  #  return app
