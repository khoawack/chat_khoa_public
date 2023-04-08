from flask import Flask, render_template, request, url_for, redirect
import function
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "asdklfsdlakfsdjklf2312"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Messages_list(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(150))
    answer = db.Column(db.String(250))
  


@app.route("/")
def home():
    db.create_all()
    return render_template('chat.html')

@app.route("/chat", methods=["GET", "POST"])
def chatting():
    if request.method == "POST":
        question = request.form["question"]
        result = function.askGPT(question)
        new_message = Messages_list(message=question, answer = result)
        db.session.add(new_message)
        db.session.commit()
        
        # Fetch message list from the database
        message_list = Messages_list.query.all()
        
        return render_template("chat.html", reply_text=str(result), message_list=message_list)
    else:
        # Fetch message list from the database
        message_list = Messages_list.query.all()
        return render_template("chat.html", message_list=message_list)


@app.route('/delete/<int:todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    message = Messages_list.query.filter_by(task_id=todo_id).first()
    if message:
        db.session.delete(message)
        db.session.commit()
    return redirect(url_for("chatting"))

@app.route('/new')
def new():
    db.session.query(Messages_list).delete()
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)