import time
import random
import math
import matplotlib.pyplot as plt
import numpy as np


class SequencialSearch:

    def __init__(self, total_numbers, valor_a_ser_encontrado):  # Estou definindo o número de valores do vetor e a chave
        self.valor_a_ser_encontrado = valor_a_ser_encontrado
        self.total_numbers = total_numbers

    # Preenchendo Vetor Ordenado
    def fill_vector_order(self):
        vector = list(range(0, self.total_numbers + 1))
        return vector

    # Preenchendo Vetor Desordenado
    def fill_vector_disorder(self):
        vector = list(range(0, self.total_numbers + 1))
        random.shuffle(vector)
        return vector

    # Busca Sequencial Simples: Podemos trabalhar tanto com o vetor ordenado quanto desordenado
    def sequence_search(self):
        vector = self.fill_vector_disorder()
        i = 0

        while i < len(vector):
            if vector[i] == self.valor_a_ser_encontrado:
                return "O elemento {} foi encontrado na posição {}".format(self.valor_a_ser_encontrado, i)

            i += 1

        return "Não foi possível encontrar o elemento {}".format(self.valor_a_ser_encontrado)

    # Busca sequencial com Sentinela: Podemos trabalhar tanto com o vetor ordenado quanto desordenado
    def sentry_sequence_search(self):
        vector = self.fill_vector_disorder()
        i = 0
        vector.append(self.valor_a_ser_encontrado)

        while vector[i] != self.valor_a_ser_encontrado:
            i += 1

        if i == len(vector) - 1:
            return "Não foi possível encontrar o elemento {}".format(self.valor_a_ser_encontrado)

        return "O elemento {} foi encontrado na posição {}".format(self.valor_a_ser_encontrado, i)

    # Busca Binária: Os elementos devem está ordenados
    def binary_search(self):
        vector = self.fill_vector_order()
        low = 0
        high = len(vector) - 1

        while low <= high:
            mid = int((low+high)/2)
            guess = vector[mid]

            if guess == self.valor_a_ser_encontrado:
                return "O elemento {} foi encontrado".format(self.valor_a_ser_encontrado)
            elif guess > self.valor_a_ser_encontrado:
                high = mid - 1
            else:
                low = mid + 1
        return "O elemento {} não foi encontrado".format(self.valor_a_ser_encontrado)


    # Busca por Interpolação: Os elementos devem está ordenados
    def interpolation_search(self):
        vector = self.fill_vector_order()
        begin = 0
        end = len(vector) - 1
        while begin <= end and vector[begin] <= self.valor_a_ser_encontrado <= vector[end]:
            i = int(begin + (((end - begin)/(vector[end] - vector[begin])) * (self.valor_a_ser_encontrado - vector[begin])))
            if vector[i] == self.valor_a_ser_encontrado:
                return "O elemento {} foi encontrado na posição {}".format(self.valor_a_ser_encontrado, i)

            if self.valor_a_ser_encontrado > vector[i]:
                begin = i + 1

            else:
                end = i - 1
        return "Não foi possível encontrar o elemento {}".format(self.valor_a_ser_encontrado)

    # Busca por salto: Similar a busca binária, funciona através de saltos
    def jump_search(self):
        lys = self.fill_vector_order()
        val = self.valor_a_ser_encontrado
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
                return "O elemento {} foi encontrado na posição {}".format(val, i)
            i += 1
        return "Não foi possível encontrar o elemento {}".format(val)

    @staticmethod
    #  Função para plotar gráficos
    def plotting_graph(total_time):
        x = np.linspace(0, total_time, 10)
        y = x
        plt.plot(x, y)
        plt.title('Time - Search Method')
        plt.xlabel('time(x 1000)')
        plt.ylabel('time(x 1000)')
        plt.savefig('method.png', bbox_inches='tight')
        plt.show()

    @staticmethod
    # Função para comparar gráficos
    def compare_graph(total_time_one, total_time_two):
        x = np.linspace(0, total_time_one, 10)
        y = x

        x_2 = np.linspace(0, total_time_two, 10)
        y_2 = x_2

        plt.subplot(1, 2, 1)
        plt.plot(x, y)
        plt.title('Time 1')
        plt.xlabel('time(x 1000)')
        plt.ylabel('time(x 1000)')

        plt.subplot(1, 2, 2)
        plt.plot(x_2, y_2, color='xkcd:salmon')
        plt.title('Time 2')
        plt.xlabel('time(x 1000)')
        plt.ylabel('time(x 1000)')

        plt.savefig('compare_methods.png', bbox_inches='tight')
        plt.show()


busca = SequencialSearch(1000, 40)  # Inicialzando o objeto

antes_one = time.time()
number_one = busca.sentry_sequence_search()
depois_one = time.time()  # Medindo o tempo

total_one = (depois_one - antes_one) * 1000  # Segundos multiplicados em 10000
print(number_one)
print("O tempo gasto foi: {:6f} mili-segundos". format(total_one))

# Plotando a comparação dos metodos
antes_two = time.time()
number_two = busca.binary_search()
depois_two = time.time()  # Medindo o tempo

total_two = (depois_two - antes_two) * 1000 # Segundos multiplicados em 10000
print(number_two)
print("O tempo gasto foi: {:6f} mili-segundos". format(total_two))
busca.compare_graph(total_one, total_two) # Passando  como argumento os tempos de cada busca





