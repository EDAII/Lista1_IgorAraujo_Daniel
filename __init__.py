from flask import Flask,render_template,request
from algoritmos import SequencialSearch
import time
import timeit
import random


app = Flask(__name__)

# Preenchendo Vetor Ordenado
def fill_vector_order(total_numbers):
    vector = list(range(0,total_numbers + 1))
    return vector
    
# Preenchendo Vetor Desordenado
def fill_vector_disorder(total_numbers):
    vector = list(range(0,total_numbers + 1))
    random.shuffle(vector)
    return vector

# Busca Sequencial Simples: Podemos trabalhar tanto com o vetor ordenado quanto desordenado
def simple_sequence_search(valor_a_ser_encontrado,total_numbers):
    vector = fill_vector_disorder(total_numbers)
    i = 0
    while i < len(vector):
        if vector[i] == valor_a_ser_encontrado:
            return "O elemento {} foi encontrado na posição {}".format(valor_a_ser_encontrado, i)
        i += 1
    return "Não foi possível encontrar o elemento {}".format(valor_a_ser_encontrado)

# Busca sequencial com Sentinela: Podemos trabalhar tanto com o vetor ordenado quanto desordenado
def sentry_sequence_search(valor_a_ser_encontrado,total_numbers):
    vector = fill_vector_order(total_numbers)
    i = 0
    vector.append(valor_a_ser_encontrado)
    while vector[i] != valor_a_ser_encontrado:
        i += 1
    if i == len(vector) - 1:
        return "Não foi possível encontrar o elemento {}".format(valor_a_ser_encontrado)
    return "O elemento {} foi encontrado na posição {}".format(valor_a_ser_encontrado, i)
   

# Busca Binária: Os elementos devem está ordenados
def binary_search(valor_a_ser_encontrado,total_numbers):
    vector = fill_vector_order(total_numbers)
    left, right, attempt = 0, len(vector), 1
    while 1:
        middle = int((left + right) / 2)
        aux_num = vector[middle]
        if valor_a_ser_encontrado == aux_num:
            return "O elemento {} foi encontrado na posição {}".format(valor_a_ser_encontrado, attempt)
        elif valor_a_ser_encontrado > aux_num:
            left = middle
        else:
            right = middle
        attempt += 1

@app.route("/")
def form():
    return render_template("home.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      #definir valores preenchidos no formulário
      total_numbers =request.form['total_numbers']
      valor_a_ser_encontrado =request.form['valor_a_ser_encontrado']
      type_search = request.form['type_search']

      #executando métodos de busca de acordo com a busca selecionada
      if type_search =='Busca Sequencial Simples':
            inicio = time.time()
            sequencia = simple_sequence_search(int(valor_a_ser_encontrado),int(total_numbers))
            fim = time.time()
            tempo = (fim-inicio)*1000
            tempo_execucao = "O tempo gasto foi: {:6f} mili-segundos". format(tempo)

      elif type_search =='Busca Sequencial Com Sentinela':
            inicio = time.time()
            sequencia = sentry_sequence_search(int(valor_a_ser_encontrado),int(total_numbers))
            fim = time.time()
            tempo = (fim-inicio)*1000
            tempo_execucao = "O tempo gasto foi: {:6f} mili-segundos". format(tempo)

      elif type_search =='Busca Binária':
            inicio = time.time()
            sequencia =binary_search(int(valor_a_ser_encontrado),int(total_numbers))
            fim = time.time()
            tempo = (fim-inicio)*1000
            tempo_execucao = "O tempo gasto foi: {:6f} mili-segundos". format(tempo)
      return render_template("result.html",tempo_execucao = tempo_execucao ,sequencia=sequencia)


if __name__ == "__main__":
    app.run(debug=True)