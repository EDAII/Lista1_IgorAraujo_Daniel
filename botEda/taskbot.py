#!/usr/bin/env python3
import json
import requests
import time
import urllib
import random
import sqlalchemy
import db
from db import Busca
import math
#library telegram
import telegram

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
def simple_sequence_search(total_numbers,valor_a_ser_encontrado):
    vector = fill_vector_disorder(total_numbers)
    i = 0
    while i < len(vector):
        if vector[i] == valor_a_ser_encontrado:
            return i
        i += 1
    return "Não foi possível encontrar o elemento {}".format(valor_a_ser_encontrado)

# Busca sequencial com Sentinela: Podemos trabalhar tanto com o vetor ordenado quanto desordenado
def sentry_sequence_search(total_numbers,valor_a_ser_encontrado):
    vector = fill_vector_order(total_numbers)
    i = 0
    vector.append(valor_a_ser_encontrado)
    while vector[i] != valor_a_ser_encontrado:
        i += 1
    if i == len(vector) - 1:
        return "Não foi possível encontrar o elemento {}".format(valor_a_ser_encontrado)
    return  i
   
# Busca Binária: Os elementos devem está ordenados
def binary_search(total_numbers,valor_a_ser_encontrado):
    vector = fill_vector_order(total_numbers)
    left, right, attempt = 0, len(vector), 1
    while 1:
        middle = int((left + right) / 2)
        aux_num = vector[middle]
        if valor_a_ser_encontrado == aux_num:
            return attempt
        elif valor_a_ser_encontrado > aux_num:
            left = middle
        else:
            right = middle
        attempt += 1

# Busca por Interpolação: Os elementos devem está ordenados
def interpolation_search(total_numbers,valor_a_ser_encontrado):
    begin = 0
    vector = fill_vector_order(total_numbers)
    end = len(vector) - 1
    while begin <= end and vector[begin] <= valor_a_ser_encontrado <= vector[end]:
        i = int(begin + (((end - begin)/(vector[end] - vector[begin])) * (valor_a_ser_encontrado - vector[begin])))
        if vector[i] == valor_a_ser_encontrado:
            return "O elemento {} foi encontrado na posição {}".format(valor_a_ser_encontrado, i)
        if valor_a_ser_encontrado > vector[i]:
            begin = i + 1
        else:
            end = i - 1

#  Função para plotar gráficos
def plotting_graph(total_numbers, total_time):
    new_time = int(round(total_time))
    time_vector = fill_vector_order_different(new_time)
    vector = fill_vector_order_different(new_time)
    plt.plot(time_vector, vector)
    plt.title('Time - Search Method')
    plt.xlabel('time(x 1000)')
    plt.ylabel('time(x 1000)')
    plt.savefig('method.png', bbox_inches='tight')
    # plt.show()

# Função para comparar gráficos
def compare_graph(self, total_time_one, total_time_two):
    new_time_one = int(round(total_time_one))
    time_vector_one = self.fill_vector_order_different(new_time_one)
    vector_one = self.fill_vector_order_different(new_time_one)
    new_time_two = int(round(total_time_two))
    time_vector_two = self.fill_vector_order_different(new_time_two)
    vector_two = self.fill_vector_order_different(new_time_two)
    plt.subplot(1, 2, 1)
    plt.plot(time_vector_one, vector_one)
    plt.title('Tempo 1')
    plt.xlabel('time(x 1000)')
    plt.ylabel('time(x 1000)')
    plt.subplot(1, 2, 2)
    plt.plot(time_vector_two, vector_two, color='xkcd:salmon')
    plt.title('Tempo 2')
    plt.xlabel('time(x 1000)')
    plt.ylabel('time(x 1000)')

    plt.show()
    plt.savefig('compare_methods.png', bbox_inches='tight')

# Busca por salto: Similar a busca binária, funciona através de saltos
def jump_search(total_numbers,valor_a_ser_encontrado):
    lys = fill_vector_order(total_numbers)
    val = valor_a_ser_encontrado
    length = len(lys)
    jump = int(math.sqrt(length))
    left, right = 0, 0
    while left < length and lys[left] <= val:
        right = min(length - 1, left + jump)
        if lys[left] <= val and lys[right] >= val:
            break
        left += jump
    if left >= length or lys[left] > val:
        return "Não foi possível encontrar o elemento {}".format(val)
    right = min(length - 1, right)
    i = left
    while i <= right and lys[i] <= val:
        if lys[i] == val:
            return i
        i += 1
    return "Não foi possível encontrar o elemento {}".format(val)

#after take out the token to other file
TOKEN = "769301141:AAEloGEFdcAJcEUMkvZR28UaAlWUCXKvdNY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(TOKEN)
HELP = """
 /new NOME
 /todo ID
 /done ID
 /doing ID
 /delete ID
 /list
 /rename ID NOME
 /dependson ID ID...
 /duplicate ID
 /priority ID PRIORITY{low, medium, high}
 /help
"""

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)

def search(search_method,positions,number,type_search,chat):
            inicio = time.time()
            posicao=search_method(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=type_search, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A {} levou *{:4f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.typeSearch,busca.tempoExecucao,busca.number,busca.positions,posicao), chat)

def handle_updates(updates):
    #andando no json para para chegar no text enviado
    for update in updates["result"]:
        if 'message' in update:
            message = update['message']
        elif 'edited_message' in update:
            message = update['edited_message']
        else:
            print('Can\'t process! {}'.format(update))
            return
        #pega o valor da mensagem mandada para o bot e a quebra
        command = message["text"].split(" ", 1)[0]
        msg = ''
        if len(message["text"].split(" ", 1)) > 1:
            msg = message["text"].split(" ", 1)[1].strip()
            positions = msg.split(" ")[0].strip()
            number=msg.split(" ")[1].strip()            
        chat = message["chat"]["id"]
        
        if command == '/BSS':
            search(simple_sequence_search,positions,number,'Busca Sequencial Simples',chat)
            # # plotting_graph(positions,tempo)
            #bot.send_photo(chat_id=chat_id, photo=url)
        elif command =='/Buscas':
            send_message("*-------> Busca Sequencial Simples(BSS)*\n*-------> Busca Sequencial Com Sentinela(BSCS)*\n*-------> Busca Sequencial Indexada(BSI)*\n*-------> Busca Binária(BB)*\n*-------> Busca Por Salto(BPS)*", chat)
            send_message(" Digite '/' a sigla entre parentêses da busca \n ex:*/BSS* (Busca Sequencial Simples)", chat)
        
        elif command =='/BSCS':
            search(sentry_sequence_search,positions,number,'Busca Sequencial Com Sentinela',chat)
                
        elif command == '/BB':
            search(binary_search,positions,number,'Busca Binária',chat)
            
        elif command == '/BPS':
            search(jump_search,positions,number,'Busca por Salto levou',chat)
            
        elif command == '/BPI':
            search(interpolation_search,positions,number,'Busca por Interpolação',chat)
            
        elif command == '/List':
            a = ''
            a += '\U0001F4CB Top Buscas\n'
            query = db.session.query(Busca).filter_by(chat=chat).order_by(Busca.tempoExecucao)
            for busca in query.all():
                a += '[[{}]] {} {}\n'.format(busca.id, busca.typeSearch,busca.tempoExecucao)

            send_message(a, chat)
            # a = ''

            # a += '\U0001F4DD _Status_\n'
            # query = db.session.query(Busca).filter_by(status='TODO', chat=chat).order_by(Busca.id)
            # a += '\n\U0001F195 *TODO*\n'
            # for task in query.all():
            #     a += '[[{}]] {}\n'.format(busca.id, busca.typeSearch)
            # query = db.session.query(Task).filter_by(status='DOING', chat=chat).order_by(Task.id)
            # a += '\n\U000023FA *DOING*\n'
            # for task in query.all():
            #     a += '[[{}]] {}\n'.format(task.id, task.name)
            # query = db.session.query(Task).filter_by(status='DONE', chat=chat).order_by(Task.id)
            # a += '\n\U00002611 *DONE*\n'
            # for task in query.all():
            #     a += '[[{}]] {}\n'.format(task.id, task.name)

            # send_message(a, chat)

def main():
    last_update_id = None

    while True:
        print("Updates")
        updates = get_updates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)

        time.sleep(0.3)


if __name__ == '__main__':
    main()

