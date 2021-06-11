import os
from flask import Flask, request, url_for, render_template, flash, redirect, send_file
from flask_bootstrap import Bootstrap
from flask_debug import Debug
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_nav import Nav
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir) + os.sep + "static\page"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:123456@localhost/atleticator"""
db = SQLAlchemy(app)
nav = Nav()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(db.Model):
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, unique=False, nullable=True)
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delete = db.Column(db.Integer, unique=False, nullable=True)
    power = db.Column(db.String(45), unique=False, nullable=True)
    dataNasc = db.Column(db.DateTime, unique=False, nullable=True)
    profilephoto = db.Column(db.String(255), unique=False, nullable=True)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUser


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.filter_by(idUser=user_id).first()
    print(user)
    return user


# class News(db.Model):
#     news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # htmlinterno = db.Column(db.String(45), unique=True, nullable=False)
#     titulo = db.Column(db.String(45), unique=False, nullable=False)
#     conteudo = db.Column(db.String(45), unique=False, nullable=False)
#     img = db.Column(db.String(255), unique=True, nullable=False)
#     # delete = db.Column(db.SmallInteger, unique=False, nullable=True)

class User_has_news(db.Model):
    user_idUser = db.Column(db.Integer, primary_key=True, nullable=False)
    news_news_id = db.Column(db.Integer, primary_key=True, nullable=False)
    new = db.Column(db.SmallInteger, unique=False, nullable=True)


class Associacao(db.Model):
    assoc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    user_idUser = db.Column(db.Integer, nullable=False)
    idAssoc = db.Column(db.String(45), unique=True, nullable=False)
    pagamento = db.Column(db.SmallInteger, unique=False, nullable=True)


class Produto(db.Model):
    produto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(45), unique=False, nullable=True)
    preco = db.Column(db.Float, unique=False, nullable=False)
    esconder = db.Column(db.SmallInteger, unique=False, nullable=True)


class Cor(db.Model):
    cor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    produto_produto_id = db.Column(db.Integer, unique=False, nullable=False)


class Tamanho(db.Model):
    tamanho_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    produto_produto_id = db.Column(db.Integer, unique=False, nullable=False)


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    psw = PasswordField('psw', validators=[DataRequired()])
    repassword = PasswordField('repassword', validators=[DataRequired()])
    # Agree = SelectFieldBase('', validators=[DataRequired])
    Submit: SubmitField = SubmitField('Submit')


@app.route("/")
def index():
    return render_template("beko/index.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if user.profilephoto == None:
        userphoto = "person.png"
    else:
        userphoto = user.profilephoto

    if request.method == "POST":
        file = request.files['gif']
        file.filename = user.username + file.filename[-4::]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        user.profilephoto = file.filename
        db.session.add(user)
        db.session.commit()

    return render_template("beko/home.html", username=user.username, userpower=user.power, userphoto=userphoto)


@app.route("/terms")
def terms():
    return render_template("beko/terms.html")


@app.route("/testelog")
@login_required
def testelog():
    return "Hello, " + current_user.username + "!", 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MyForm()
    error = []
    power = 0

    # print (form.validate_on_submit())
    if form.validate_on_submit():
        if form.psw.data != form.repassword.data:
            error.append("The passwords do not match")
        if Users.query.filter_by(username=form.username.data).first() is not None:
            error.append("The user already exists")
        if Users.query.filter_by(email=form.email.data).first() is not None:
            error.append("The email already exists")
        if form.email.data.find('@') == -1:
            error.append("The email is invalid")
        if Users.query.filter_by().first() == None:
            power = "1"

        if error:
            flash(', '.join(error))
            return redirect(url_for('register'))
        else:
            user = Users(username=form.username.data, password=form.psw.data, email=form.email.data, power=power)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('/beko/userregisterwtf.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        user = Users.query.filter_by(username=request.form['username']).first()
        if user is not None and request.form['password'] == user.password:
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)

            return "Logged in successfully."
        return "Login Failed!"

    return render_template('/beko/login.html')  # , form=form))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    form = CadastroForm()
    if form.validate_on_submit():
        n = News()
        form.populate_obj(n)
        db.session.add(n)
        db.session.commit()

        if form.validate_on_submit():
            news = News.query.filter_by(titulo=n.titulo).first()
            f = form.img.data
            filename = secure_filename(f.filename)
            f.filename = str(news.news_id) + 'news' + f.filename[-4::]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            news.img = f.filename
            db.session.add(news)
            db.session.commit()

    return render_template("/beko/cadastro.html", form=form)


@app.route("/lista")
def lista():
    news = News.query.all()
    return render_template("/beko/lista.html", news=news)


@app.route('/get-file/<filename>')
def getFile(filename):
    file = os.path.join(UPLOAD_FOLDER, filename + '.png')
    news = News.query.filter_by(img=request.form['img']).first()
    return send_file(file, mimetype="imagem/png")


@app.route("/atualizar/<int:id>", methods=["GET", "POST"])
def atualizar(id):
    form = CadastroForm()
    news = News.query.filter_by(news_id=id).first()

    if form.validate_on_submit():
        form.populate_obj(news)
        db.session.commit()

    form = CadastroForm()
    form.insert_data(news)
    return render_template("/beko/atualizar.html", form=form)


@app.route("/excluir/<int:id>")
def excluir(id):
    news = News.query.filter_by(news_id=id).first()
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('lista'))


class CadastroForm(FlaskForm):
    titulo = StringField("Titulo:", validators=[DataRequired()])
    conteudo = TextAreaField("Conteúdo:", validators=[DataRequired()])
    img = FileField("Imagem:", validators=[FileRequired()])

    def insert_data(self, news):
        self.titulo.data = news.titulo
        self.conteudo.data = news.conteudo
        self.img.data = news.img


class News(db.Model):
    __tablename__ = "news"
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String)
    conteudo = db.Column(db.String)
    img = db.Column(db.String)


app.run(debug=True, host='localhost')
