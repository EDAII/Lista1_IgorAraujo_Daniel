from flask import Flask,render_template

app = Flask(__name__)

def soma_test(a,b):
    return a+b

#decorator onde pode ser setado a rota que será criada 
@app.route("/")
def soma():
    resultado = soma_test(1,2)
    return render_template("soma.html",resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)