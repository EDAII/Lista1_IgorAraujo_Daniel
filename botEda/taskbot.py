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
    vector = fill_vector_order(total_numbers)
    begin = 0
    end = len(vector) - 1
    while begin <= end and vector[begin] <= valor_a_ser_encontrado <= vector[end]:
        i = int(begin + (((end - begin)/(vector[end] - vector[begin])) * (valor_a_ser_encontrado - vector[begin])))
        if vector[i] == valor_a_ser_encontrado:
            return "O elemento {} foi encontrado na posição {}".format(valor_a_ser_encontrado, i)
        if valor_a_ser_encontrado > vector[i]:
            begin = i + 1
        else:
            end = i - 1

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
            msg_final = msg.split(" ")[0].strip()
            positions=msg.split(" ")[1].strip()
            number=msg.split(" ")[2].strip()
            
        chat = message["chat"]["id"]

        #print(command, msg_final, chat,positions,number)

        if command == '/BSS':
            inicio = time.time()
            posicao=simple_sequence_search(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=msg_final, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A Busca Sequencial Simples levou *{:6f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.tempoExecucao,busca.number,busca.positions,posicao), chat)
#            print('TE')  
            #send_message('Numero não está em nenhuma posição do vetor',chat)
        elif command =='/Buscas':
            send_message("*-------> Busca Sequencial Simples(BSS)*\n*-------> Busca Sequencial Com Sentinela(BSCS)*\n*-------> Busca Sequencial Indexada(BSI)*\n*-------> Busca Binária(BB)*", chat)
            send_message(" Digite '/' a sigla entre parentêses da busca \n ex:*/BSS* (Busca Sequencial Simples)", chat)
        
        elif command =='/BSCS':
            inicio = time.time()
            posicao=sentry_sequence_search(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=msg_final, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A Busca Sequencial Com Sentinela levou *{:6f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.tempoExecucao,busca.number,busca.positions,posicao), chat)
         
                
        elif command == '/BB':
            inicio = time.time()
            posicao=binary_search(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=msg_final, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A Busca Binária levou *{:6f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.tempoExecucao,busca.number,busca.positions,posicao), chat)
        elif command == '/BPS':
            inicio = time.time()
            posicao=jump_search(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=msg_final, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A Busca por Salto levou *{:6f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.tempoExecucao,busca.number,busca.positions,posicao), chat)
            
        elif command == '/BPI':
            inicio = time.time()
            posicao=interpolation_search(int(positions),int(number))
            fim = time.time()
            tempo = (fim-inicio)*1000
            busca = Busca(chat=chat, typeSearch=msg_final, positions=int(positions),number=int(number),tempoExecucao=float(tempo))
            db.session.add(busca)
            db.session.commit()
            send_message("A Busca por Interpolação levou *{:6f}* milisegundos para buscar o valor *{}* em um vetor de {} posições na posição *{}*".format(busca.tempoExecucao,busca.number,busca.positions,posicao), chat)

def main():
    last_update_id = None

    while True:
        print("Updates")
        updates = get_updates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)

        time.sleep(0.5)


if __name__ == '__main__':
    main()

