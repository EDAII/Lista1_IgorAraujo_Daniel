def print_search(search_list):
    one = "BSS"
    two = "BSCS"
    three = "BB"
    four = "BPS"
    five = "BPI"
    new_list = []
    for search in search_list:
        if search == one:
            aux = "Busca Sequencial Simples"
            new_list.append(aux)
        elif search == two:
            aux = "Busca Sequencial Com Sentinela"
            new_list.append(aux)
        elif search == three:
            aux = "Busca Sequencial Com Sentinela"
            new_list.append(aux)
        elif search == four:
            aux = "Busca Sequencial Com Sentinela"
            new_list.append(aux)
        elif search == five:
            aux = "Busca Sequencial Com Sentinela"
            new_list.append(aux)
    return new_list 

b = "/BSS@BSCS"
b_n = b.replace("@", " ")
b_new = b_n.replace("/", " ")
search_list = b_new.split()
list_names = print_search(search_list)

for i in list_names:
    print(i)


