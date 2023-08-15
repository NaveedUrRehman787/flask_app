
from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login_systemsss.db"
app.secret_key = "m0,9n7.87.8"

db = SQLAlchemy(app)
app.app_context().push()

class BlogPosts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=True)
    password = db.Column(db.Text,nullable=True)
    author = db.Column(db.String(50),nullable=True)
    subject = db.Column(db.String(50),nullable=True)
    category = db.Column(db.String(50),nullable=True)
 
    

class LoginSystem(db.Model):
    ## Login System
    id = db.Column(db.Integer,primary_key=True)
    actual_user = db.Column(db.String(50),nullable=True)
    password_hash = db.Column(db.String(128),nullable=True)

    def set_password(self,passwd):
        self.password_hash = generate_password_hash(passwd)

    def check_password(self,passwd):
        return check_password_hash(self.password_hash,passwd)

@app.route("/posts",methods=["GET","POST"])
def post():
    if request.method == "POST":
       user_name = request.form.get("username")
       pass_word = request.form.get("password")
       author_ = request.form.get("author")
       subject_ = request.form.get("subject")
       category_ = request.form.get("category")

       
       new_post = BlogPosts(username=user_name,password=pass_word,
                            author=author_,subject=subject_,category=category_)
       if new_post:
          db.session.add(new_post)
          db.session.commit()
       return redirect("/posts")
    else:
        all_posts = BlogPosts.query.all()
        return render_template("posts.html",posts=all_posts)


### Create a Registration Route
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("actual_user")
        password = request.form.get("password_hash")

        existing_user = LoginSystem.query.filter_by(actual_user=username).first()
        if existing_user:
            return "Username already taken. Please choose another"
        
        new_user = LoginSystem(actual_user=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print("It's look like that it is working")

        return redirect("/login")
    return render_template("register.html")


## Create a Login Route
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("actual_user")
        password = request.form.get("password_hash")

        user = LoginSystem.query.filter_by(actual_user=username).first()

        if user and user.check_password(password):
           session["user_id"] = user.id
           flash("Login successful!","success")
           return redirect("/posts")
        else:
           flash("Invalid username or password")

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/login")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)