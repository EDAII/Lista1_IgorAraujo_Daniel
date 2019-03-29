#!/usr/bin/env python3
import time
from botConfig import get_url,get_updates,get_json_from_url,get_last_update_id,send_message
from searchMethods import simple_sequence_search,sentry_sequence_search,jump_search,interpolation_search,binary_search
from searchMethods import fill_vector_order_different,fill_vector_order,fill_vector_disorder
from searchMethods import plotting_graph,compare_graph,search
import telegram

TOKEN = "769301141:AAEloGEFdcAJcEUMkvZR28UaAlWUCXKvdNY"
bot = telegram.Bot(TOKEN)
     
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
        chat = message["chat"]["id"]
        if len(message["text"].split(" ", 1)) > 1:
            try:
                msg = message["text"].split(" ", 1)[1].strip()
                positions = msg.split(" ")[0].strip()
                number=msg.split(" ")[1].strip()
            except:
                return send_message('Somente um argumento foi passado para o calculo da busca',chat)
        
        if command =='/Buscas':
            send_message("*-------> Busca Sequencial Simples(BSS)*\n*-------> Busca Sequencial Com Sentinela(BSCS)*\n*-------> Busca Sequencial Indexada(BSI)*\n*-------> Busca Binária(BB)*\n*-------> Busca Por Salto(BPS)*", chat)
            send_message(" Digite '/' a sigla entre parentêses da busca \n ex:*/BSS* (Busca Sequencial Simples)", chat)
        
        elif command == '/BSS':
            search(simple_sequence_search,positions,number,'Busca Sequencial Simples',chat)
            bot.send_photo(chat_id=chat, photo=open('./method.png', 'rb'))
        
        elif command =='/BSCS':
            search(sentry_sequence_search,positions,number,'Busca Sequencial Com Sentinela',chat)
            bot.send_photo(chat_id=chat, photo=open('./method.png', 'rb'))    
        elif command == '/BB':
            search(binary_search,positions,number,'Busca Binária',chat)
            
        elif command == '/BPS':
            search(jump_search,positions,number,'Busca por Salto levou',chat)
            
        elif command == '/BPI':
            search(interpolation_search,positions,number,'Busca por Interpolação',chat)
            
        elif command == '/BSS@BSCS':
            try:
                first_time=search(simple_sequence_search,positions,number,'Busca Sequencial Simples',chat)
                second_time=search(sentry_sequence_search,positions,number,'Busca Sequencial Com Sentinela',chat)
                compare_graph(first_time,second_time)
                bot.send_photo(chat_id=chat, photo=open('./compare_methods.png', 'rb'))
                if first_time > second_time:    
                    eficiencia = (first_time/second_time)
                    send_message('A busca sequencial simpes foi {}vezes mais rápida que a com sentinela'.format(int(eficiencia)),chat)
                elif first_time < second_time:
                    eficiencia = (second_time/first_time)
                    send_message('A busca sequencial com sentinela foi {} vezes mais rápida que a busca sequencial simples'.format(int(eficiencia)),chat)
            except:
                return send_message('OPS.... algum argumento foi passado errado,tente novamente',chat)
        
        elif command == 'BSS@BB':
            first_time=search(simple_sequence_search,positions,number,'Busca Sequencial Simples',chat)
            second_time=search(binary_search,positions,number,'Busca Binária',chat)
            compare_graph(first_time,second_time)
            bot.send_photo(chat_id=chat, photo=open('./compare_methods.png', 'rb'))
            
        # elif command == 'BSS@BPI':
            first_time=search(simple_sequence_search,positions,number,'Busca Sequencial Simples',chat)
            second_time=search(interpolation_search,number,positions,'Busca por Interpolação',chat)
            compare_graph(first_time,second_time)
            bot.send_photo(chat_id=chat, photo=open('./compare_methods.png', 'rb'))
        # elif command == 'BSS@BPI':

        # elif command == 'BSCS@BSS':

        # elif command == 'BSCS@BB':
        
        # elif command == 'BSCS@BPS':

        # elif command == 'BSCS@BPI':

        # elif command == 'BB@BSS':

        # elif command == 'BB@BSCS':
        
        # elif command == 'BB@BPI':

        # elif command == 'BPS@BSS':

        # elif command == 'BPS@BPI':
        
        # elif command == 'BPS@BSCS':

        # elif command == 'BPS@BB':

        elif command == '/List':
            a = ''
            a += '\U0001F4CB Top Buscas\n'
            query = db.session.query(Busca).filter_by(chat=chat).order_by(Busca.tempoExecucao)
            for busca in query.all():
                a += '[[{}]] {} {}\n'.format(busca.id, busca.typeSearch,busca.tempoExecucao)
            send_message(a, chat)

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

