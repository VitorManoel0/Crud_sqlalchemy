from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'

db = SQLAlchemy(app)

class Empresa(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    local = db.Column(db.String(150))
    funcionario = db.relationship('Funcionario', backref = 'empresa', lazy = True, cascade = 'all, delete-orphan')
    def __init__(self, nome,local):
        self.nome = nome
        self.local = local

class Funcionario(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    cargo = db.Column(db.String(150))
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"),nullable=False)
    def __init__(self, nome,cargo,empresa_id):
        self.nome = nome
        self.cargo = cargo
        self.empresa_id = empresa_id


@app.route('/', methods=['GET', 'POST'])
def home():
    empresa_nome = []
    db.create_all()
    empresa = Empresa.query.all()
    funcionario = Funcionario.query.all()
    for i in db.session.query(Empresa.id).all():
        empresa_nome.append(db.session.query(Empresa.nome, Empresa.id).filter_by(id=i.id).all())
    return render_template('index.html',funcionario = funcionario, empresa = empresa, empresa_nome = empresa_nome)

@app.route('/add/empresa', methods=['GET', 'POST'])
def add_empresa():
    if request.method == 'POST':
        empresa = Empresa(request.form['nome'],request.form['local'])
        db.session.add(empresa)
        db.session.commit()
        return redirect('/')
    return render_template('add_empresa.html')

@app.route('/add/funcionario', methods=['GET', 'POST'])
def add_funcionario():
    empresa = Empresa.query.all()
    if request.method == 'POST':
        funcionario = Funcionario(request.form['nome'],request.form['cargo'], request.form['empresa_id'])
        db.session.add(funcionario)
        db.session.commit()
        return redirect('/')
    return render_template('add_func.html', empresa = empresa)

@app.route('/delete/func/<int:id>')
def delete_funcionario(id):
    funcionario = Funcionario.query.get(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect('/')

@app.route('/delete/empre/<int:id>')
def delete_empresa(id):
    empresa = Empresa.query.get(id)
    db.session.flush()
    db.session.delete(empresa)
    db.session.commit()
    return redirect('/')

@app.route('/edit/func/<int:id>', methods=['GET', 'POST'])
def edit_funcionario(id):
    funcionario = Funcionario.query.get(id)
    empresa = Empresa.query.all()
    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        funcionario.cargo = request.form['cargo']
        funcionario.empresa_id = request.form['empresa_id']
        db.session.commit()
        return redirect('/')
    return render_template('edit_func.html', funcionario = funcionario, empresa = empresa)

@app.route('/edit/empre/<int:id>', methods=['GET', 'POST'])
def edit_empresa(id):
    empresa = Empresa.query.get(id)
    if request.method == 'POST':
        empresa.nome = request.form['nome']
        empresa.local = request.form['local']
        db.session.commit()
        return redirect('/')
    return render_template('edit_empresa.html', empresa = empresa)

if __name__ == '__main__':
    app.run()
