from flask import Flask, request,render_template,redirect,url_for,session
from datetime import datetime

app=Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.route("/")
def index():
    if 'inscritos' not in session:
        session['inscritos'] = []
    
    inscritos =  session.get('inscritos',[])
    return render_template('index.html',inscritos=inscritos)

def generar_id():
    if 'inscritos' in session and len(session['inscritos'])>0:
        return max(item['id'] for item in session ['inscritos'])+1
    else:
        return 1



@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        fecha=request.form['fecha']
        nombre =request.form['nombre']
        apellidos =request.form['apellidos']
        turno=request.form['turno']
        seminarios =request.form['seminarios']

        nuevo_inscrito={
            'id':generar_id(),
            'fecha':fecha,
            'nombre':nombre,
            'apellidos':apellidos,
            'turno':turno,
            'seminarios':seminarios
        }

        if 'inscritos' not in session:
            session['inscritos']=[]

        session['inscritos'].append(nuevo_inscrito)
        session.modified=True
        return redirect(url_for('index'))


    return render_template('nuevo.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_inscritos = session.get('inscritos',[])
    inscrito=next(( c for c in lista_inscritos if c['id']==id),None)
    if not inscrito:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        inscrito['nombre']=request.form['nombre']
        inscrito['fecha']=request.form['fecha']
        inscrito['apellidos'] =request.form['apellidos']
        inscrito['turno'] =request.form['turno']
        inscrito['seminarios'] =request.form['seminarios']
        session.modified =True
        return redirect(url_for('index'))

    return render_template('editar.html',inscrito=inscrito)


@app.route("/eliminar/<int:id>",methods =["POST"])
def eliminar(id):
    lista_inscritos =session.get('inscritos',[])
    inscrito =next((c for c in lista_inscritos if c['id']==id),None)
    if inscrito:
        session['inscritos'].remove(inscrito)
        session.modified =True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)