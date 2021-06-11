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
from datetime import datetime




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir) + os.sep + "static\page"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:6=2Cxl{3t6}g[pD@localhost/atleticator"""
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
    admultimochat = db.Column(db.Integer,  unique=False, nullable=True)

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


class News(db.Model):
    news_id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(255), unique=True, nullable=True)
    htmlinterno = db.Column(db.String(45), unique=True, nullable=True)
    titulo = db.Column(db.String(45), unique=False, nullable=False)
    data = db.Column(db.TIMESTAMP(6), unique=False, nullable=True)

class Chatstats(db.Model):
    idtable1 =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    buynew =  db.Column(db.Integer, unique=False, nullable=True)
    admnew =  db.Column(db.Integer, unique=False, nullable=True)
    users_idUser =  db.Column(db.Integer, unique=True, nullable=False)

class User_has_news(db.Model):
    user_has_news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_idUser = db.Column(db.Integer, unique=False, nullable=False)
    news_news_id = db.Column(db.Integer, unique=False, nullable=False)
    new = db.Column(db.SmallInteger,  unique=False, nullable=True)


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
    esconder = db.Column(db.SmallInteger,  unique=False, nullable=True)
    imagem = db.Column(db.String(45), unique=True, nullable=True)

class Cor(db.Model):
    cor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Produto_has_cor(db.Model):
    produto_has_cor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cor_cor_id = db.Column(db.Integer,unique=False, nullable=False)
    produto_produto_id = db.Column(db.Integer, unique=False, nullable=False)


class Tamanho(db.Model):
    tamanho_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Produto_has_tamanho(db.Model):
    produto_has_tamanho_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tamanho_tamanho_id = db.Column(db.Integer, unique=False, nullable=False)
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


@app.route("/loja", methods=["GET", "POST"])
def loja():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    userphoto = user.profilephoto
    if user.profilephoto == None:
        userphoto = "person.png"


    relacaodeprodutosvisiveis = {'headers': ['id', 'nome', 'descricao', 'preco', 'tamanhos', 'cores', 'img'],
                             'contents': []
                              }
    relacaodetamanhos = {'headers': ['tamanho'],
                             'contents': []
                              }
    relacaodecores = {'headers': ['cor'],
                             'contents': []
                              }

    for cadatamanho in Tamanho.query.filter_by():
        dic= {'tamanho':cadatamanho.name}
        relacaodetamanhos['contents'].append(dic)

    for cadacor in Cor.query.filter_by():
        dic = {'cor': cadacor.name}
        relacaodecores['contents'].append(dic)



    produtosdisponiveis = Produto.query.filter_by(esconder=None)

    for produtovisivel in produtosdisponiveis:
        relacaodecoresdoproduto = {'headers': ['cor'],
                             'contents': []
                              }
        relacaodetamanhosdoproduto = {'headers': ['tamanho'],
                             'contents': []
                              }
        coresdoproduto =  Produto_has_cor.query.filter_by(produto_produto_id=produtovisivel.produto_id)
        for cordoproduto in coresdoproduto:
            nomedacor = Cor.query.filter_by(cor_id=cordoproduto.cor_cor_id).first()
            dic = {'cor': nomedacor.name}
            relacaodecoresdoproduto['contents'].append(dic)

        tamanhosdoproduto = Produto_has_tamanho.query.filter_by(produto_produto_id=produtovisivel.produto_id)
        for tamanhodoproduto in tamanhosdoproduto:
            nomedotamanho = Tamanho.query.filter_by(tamanho_id=tamanhodoproduto.tamanho_tamanho_id).first()
            dic = {'tamanho': nomedotamanho.name}
            relacaodetamanhosdoproduto['contents'].append(dic)

        imagem = produtovisivel.imagem
        if produtovisivel.imagem == None:
            imagem = "Ecommerce-Product-icon.png"
        dic = {
            'id': produtovisivel.produto_id,
            'nome': produtovisivel.name,
            'descricao': produtovisivel.descricao,
            'preco': produtovisivel.preco,
            'tamanhos': relacaodetamanhosdoproduto,
            'cores': relacaodecoresdoproduto,
            'img': imagem,
        }
        relacaodeprodutosvisiveis['contents'].append(dic)

    if request.method == "POST":
        erro = 0
        if request.form["name"] == "":
            erro = 1
            flash("Digite um nome")
        if Produto.query.filter_by(name=request.form["name"]).first() is not None:
            erro = 1
            flash("Esse produto já existe")
        if request.form["preco"] == "":
            erro = 1
            flash("Digite um preço")
        if erro == 0:
            print(request)
            novoproduto = Produto()
            novoproduto.name = request.form["name"]
            novoproduto.descricao = request.form["descricao"]
            novoproduto.preco = request.form["preco"]
            novoproduto.preco = float(novoproduto.preco.replace(",", "."))
            file = request.files['fotodoproduto']
            if file.filename[-4::] == "":
                print("produto sem imagem")
            else:
                file.filename = "produto" + request.form["name"] + file.filename[-4::]
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                novoproduto.imagem = file.filename
            db.session.add(novoproduto)
            db.session.commit()
            for itemdoformulario in request.form:
                if itemdoformulario.count('-') > 0:
                    if "cor" == (itemdoformulario.split('-')[0]):
                        relacaodacorcomoproduto = Produto_has_cor()
                        coraserinseridadoproduto = Cor.query.filter_by(name=(itemdoformulario.split('-')[1])).first()
                        novoprodutonobanco = Produto.query.filter_by(name=novoproduto.name).first()
                        relacaodacorcomoproduto.cor_cor_id = coraserinseridadoproduto.cor_id
                        relacaodacorcomoproduto.produto_produto_id = novoprodutonobanco.produto_id
                        db.session.add(relacaodacorcomoproduto)
                        db.session.commit()
                        flash("Cor " + itemdoformulario.split('-')[0] + " adicionado com sucesso ao "+ novoprodutonobanco.name)
                    if "tamanho" == (itemdoformulario.split('-')[0]):
                        relacaodatamanhocomoproduto = Produto_has_tamanho()
                        tamanhoaserinseridadoproduto = Tamanho.query.filter_by(name=(itemdoformulario.split('-')[1])).first()
                        novoprodutonobanco = Produto.query.filter_by(name=novoproduto.name).first()
                        relacaodatamanhocomoproduto.tamanho_tamanho_id = tamanhoaserinseridadoproduto.tamanho_id
                        relacaodatamanhocomoproduto.produto_produto_id = novoprodutonobanco.produto_id
                        db.session.add(relacaodatamanhocomoproduto)
                        db.session.commit()
                        flash("Tamanho "+itemdoformulario.split('-')[0]+" adicionado com sucesso ao "+ novoprodutonobanco.name)
        flash("Produto adicionado com sucesso.")

    statusdochat = Chatstats.query.filter_by(users_idUser=user.idUser).first()

    return render_template("beko/loja.html", username=user.username , userpower=user.power, userphoto=userphoto,
                           produtos=relacaodeprodutosvisiveis,
                           tamanhos=relacaodetamanhos,
                           cores=relacaodecores, chatstatus=statusdochat.admnew)

@app.route("/lojacomprachat", methods=["GET", "POST"])
def lojacomprachat():
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        try:
            nome_arquivo = "templates/chat/"+str(user.idUser)+".html"
            arquivo = open(nome_arquivo, 'r+')
        except FileNotFoundError:
            arquivo = open(nome_arquivo, 'w+')
        mensagemanteriores = arquivo.read()
        arquivo.write(str(today)+" <b>"+str(user.username)+"</b> disse: Olá, fiquei interessado em um " + request.form["nome"] + " do tamanho " + request.form["tamanho"] + " e da cor " + request.form["cor"]+". Ele custa R$" + request.form["preco"] + " na loja.<br><br>")
        # faca o que quiser
        arquivo.close()
        statusdochat = Chatstats.query.filter_by(users_idUser=user.idUser).first()
        statusdochat.buynew = 1
        db.session.add(statusdochat)
        db.session.commit()
    return redirect('/loja')

@app.route("/chatresponde", methods=["GET", "POST"])
def chatresponde():
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        donodochat = Users()
        iddodono = request.form["username"].replace("/chat/","")
        if Users.query.filter_by(idUser=iddodono).first():
            donodochat = Users.query.filter_by(idUser=iddodono).first()
        else:
            donodochat = Users.query.filter_by(username=request.form["username"]).first()

        nome_arquivo = "templates/chat/"+str(donodochat.idUser)+".html"
        arquivo = open(nome_arquivo, 'r+')
        mensagemanteriores = arquivo.read()
        arquivo.write(str(today)+" <b>"+str(user.username)+"</b> disse: "+request.form["mensagem"]+"<br><br>")
        # faca o que quiser
        arquivo.close()

        statusdochat = Chatstats.query.filter_by(users_idUser=donodochat.idUser).first()
        if user.idUser == donodochat.idUser:
            statusdochat.buynew = 1
            statusdochat.admnew = 0
            db.session.add(statusdochat)
            db.session.commit()
            return redirect('/loja')
        else:
            user.admultimochat = donodochat.idUser
            statusdochat.admnew = 1
            statusdochat.buynew = 0
            db.session.add(statusdochat)
            db.session.commit()
            return redirect('/admchat')

@app.route("/admchat", methods=["GET", "POST"])
def admchat():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    lastchat = 0
    if user.admultimochat == None:
        lastchat = user.idUser
    else:
        lastchat = user.admultimochat
    if user.power == "1":
        allusers = {'headers': ['idUser', 'unsername', 'chatstatus'],
                             'contents': []
                              }
        for eachuser in Users.query.filter_by():
            statusdochat = Chatstats.query.filter_by(users_idUser=eachuser.idUser).first()
            dic = {
                'idUser': eachuser.idUser,
                'username': eachuser.username,
                'chatstatus': statusdochat.buynew,
            }
            allusers['contents'].append(dic)
        return render_template("admchat.html", allusers=allusers, ultimochat=lastchat )
    else:
        return "Você não pode ver essa página."

@app.route("/chat/<string:PageAddresi>", methods=["GET", "POST"])
def route_page(PageAddresi):
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if user.power == "1":
        chat = open("templates/chat/" + str(PageAddresi) + ".html", "r")
        return chat.read()
    else:
        return "Você não pode ver essa página."

@app.route("/chat", methods=["GET", "POST"])
def chat():

    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    chat = open("templates/chat/"+str(user.idUser)+".html", "r")
    return chat.read()


@app.route("/lojacor", methods=["GET", "POST"])
def lojacor():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        if int(user.power) < 1:
            flash("Você não pode fazer isso")
        else:
            novacor = Cor()
            novacor.name = request.form["name"]
            db.session.add(novacor)
            db.session.commit()
            flash("Cor adicionada com sucesso.")

    return redirect('/loja')

@app.route("/deletecor", methods=["GET", "POST"])
def deletecor():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        if int(user.power) < 1:
            flash("Você não pode fazer isso")
        else:
            essacor = Cor.query.filter_by(name=request.form["name"]).first()
            coresdoproduto = Produto_has_cor.query.filter_by(cor_cor_id=essacor.cor_id)
            for cdp in coresdoproduto:
                db.session.delete(cdp)
            db.session.delete(essacor)
            db.session.commit()
            flash("Cor deletada com sucesso.")

    return redirect('/loja')

@app.route("/deleteproduto", methods=["GET", "POST"])
def deleteproduto():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        if int(user.power) < 1:
            flash("Você não pode fazer isso")
        else:
            esseproduto = Produto.query.filter_by(name=request.form["name"]).first()
            coresdoproduto = Produto_has_cor.query.filter_by(produto_produto_id=esseproduto.produto_id)
            for cdp in coresdoproduto:
                db.session.delete(cdp)
                db.session.commit()
            tamanhosdoproduto = Produto_has_tamanho.query.filter_by(produto_produto_id=esseproduto.produto_id)
            for tdp in tamanhosdoproduto:
                db.session.delete(tdp)
                db.session.commit()
            db.session.delete(esseproduto)
            db.session.commit()
            flash("Produto deletado com sucesso.")

    return redirect('/loja')

@app.route("/deletetamanho", methods=["GET", "POST"])
def deletetamanho():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        if int(user.power) < 1:
            flash("Você não pode fazer isso")
        else:
            essetamanho = Tamanho.query.filter_by(name=request.form["name"]).first()
            coresdoproduto = Produto_has_tamanho.query.filter_by(tamanho_tamanho_id=essetamanho.tamanho_id)
            for tdp in coresdoproduto:
                db.session.delete(tdp)
            db.session.delete(essetamanho)
            db.session.commit()
            flash("Tamanho deletado com sucesso.")

    return redirect('/loja')

@app.route("/lojatamanho", methods=["GET", "POST"])
def lojatamanho():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if request.method == "POST":
        if int(user.power) < 1:
            flash("Você não pode fazer isso")
        else:
            novotamanho = Tamanho()
            novotamanho.name = request.form["name"]
            db.session.add(novotamanho)
            db.session.commit()
            flash("Tamanho adicionado com sucesso.")

    return redirect('/loja')



@app.route("/home", methods=["GET", "POST"])
def home():
    user = Users.query.filter_by(idUser=str(current_user).strip('<>').replace('Users ', '')).first()
    if user.profilephoto == None:
        userphoto = "person.png"
    else:
        userphoto = user.profilephoto


    if request.method == "POST":
        file = request.files['gif']
        file.filename = "user" + user.username + file.filename[-4::]
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

            esseuser = Users.query.filter_by(username=form.username.data).first()
            chatdouser = Chatstats(users_idUser=esseuser.idUser)
            db.session.add(chatdouser)
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



            try:
                nome_arquivo = "templates/chat/" + str(user.idUser) + ".html"
                arquivo = open(nome_arquivo, 'r+')
            except FileNotFoundError:
                arquivo = open(nome_arquivo, 'w+')

            #next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #    return abort(400)


            return "Logged in successfully."
        return "Login Failed!"

    return render_template('/beko/login.html')  # , form=form))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'


@app.route("/cadastrarnews", methods=["GET", "POST"])
def cadastrarnews():
    form = CadastroForm()
    if form.validate_on_submit():
        #passar parametros para o N
        if News.query.filter_by(titulo=request.form["titulo"]).first() == None:
            n = News()
            n.titulo = request.form["titulo"]
            db.session.add(n)
            db.session.commit()
            news = News.query.filter_by(titulo=n.titulo).first()
            nome_arquivo = "templates/news/" + str(news.news_id) + ".html"
            try:
                arquivo = open(nome_arquivo, 'r+')
            except FileNotFoundError:
                arquivo = open(nome_arquivo, 'w+')

            arquivo = open(nome_arquivo, 'r+')
            mensagemanteriores = arquivo.read()
            arquivo.write(request.form["conteudo"])
            # faca o que quiser
            arquivo.close()
            news.htmlinterno = nome_arquivo


            if form.validate_on_submit():
                f = form.img.data
                filename = secure_filename(f.filename)
                f.filename = str(news.news_id) + 'news' + f.filename[-4::]
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                news.img = f.filename
                db.session.add(news)
                db.session.commit()
                flash("noticia cadastrada com sucesso!")
                return redirect(url_for('home'))


    return render_template("/beko/cadastro.html", form=form)


@app.route("/listanews")
def listanews():
    news = News.query.all()
    return render_template("/beko/lista.html", news=news)


@app.route('/get-filenews/<filename>')
def getFilenews(filename):
    file = os.path.join(UPLOAD_FOLDER, filename + '.png')
    news = News.query.filter_by(img=request.form['img']).first()
    return send_file(file, mimetype="imagem/png")


@app.route("/atualizarnews/<int:id>", methods=["GET", "POST"])
def atualizarnews(id):
    form = CadastroForm()
    news = News.query.filter_by(news_id=id).first()

    if form.validate_on_submit():
        news.titulo = request.form["titulo"]
        nome_arquivo = "templates/news/" + str(news.news_id) + ".html"
        arquivo = open(nome_arquivo, 'r+')
        mensagemanteriores = arquivo.read()
        arquivo.write(request.form["conteudo"])
        # faca o que quiser
        arquivo.close()
        db.session.add(news)
        db.session.commit()

    form = CadastroForm()
    form.titulo = news.titulo
    form.img = news.img
    return render_template("/beko/atualizar.html", form=form, conteudo=news.htmlinterno)


@app.route("/excluirnews/<int:id>")
def excluirnews(id):
    news = News.query.filter_by(news_id=id).first()
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('listanews'))

@app.route("/conteudonews/<string:PageAddresi>", methods=["GET", "POST"])
def conteudonews(PageAddresi):

    conteudonews = open("templates/news/" + str(PageAddresi) + ".html", "r")
    return conteudonews.read()



class CadastroForm(FlaskForm):
    titulo = StringField("Titulo:", validators=[DataRequired()])
    conteudo = TextAreaField("Conteúdo:", validators=[DataRequired()])
    img = FileField("Imagem:", validators=[FileRequired()])

    def insert_data(self, news):
        self.titulo.data = news.titulo
        self.conteudo.data = news.conteudo
        self.img.data = news.img



app.run(debug=True, host='localhost')
