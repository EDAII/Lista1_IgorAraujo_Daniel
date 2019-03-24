import time
import random
import math
import matplotlib.pyplot as plt


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
        vector = self.fill_vector_order()
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
        left, right, attempt = 0, len(vector), 1

        while 1:
            middle = int((left + right) / 2)
            aux_num = vector[middle]
            if self.valor_a_ser_encontrado == aux_num:
                return "O elemento {} foi encontrado na posição {}".format(self.valor_a_ser_encontrado, attempt)
            elif self.valor_a_ser_encontrado > aux_num:
                left = middle
            else:
                right = middle
            attempt += 1

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

    #  Função para plotar gráficos
    def plotting_graph(self, total_time):
        vector = self.fill_vector_order()
        plt.plot(total_time, vector)
        plt.title('Search Method x Time')
        plt.xlabel('time')
        plt.ylabel('vector')
        plt.show()

    #  Busca por fibonacci : Similar a busca binária e a Busca por salto
    # def fibMonaccian_search(self):
    #
    #     # Initialize fibonacci numbers
    #     arr = self.fill_vector_order
    #     x = self.valor_a_ser_encontrado
    #     n = self.total_numbers
    #     fibMMm2 = 0  # (m-2)'th Fibonacci No.
    #     fibMMm1 = 1  # (m-1)'th Fibonacci No.
    #     fibM = fibMMm2 + fibMMm1  # m'th Fibonacci
    #
    #     # fibM is going to store the smallest
    #     # Fibonacci Number greater than or equal to n
    #     while fibM < n:
    #         fibMMm2 = fibMMm1
    #         fibMMm1 = fibM
    #         fibM = fibMMm2 + fibMMm1
    #
    #         # Marks the eliminated range from front
    #     offset = -1
    #
    #     # while there are elements to be inspected.
    #     # Note that we compare arr[fibMm2] with x.
    #     # When fibM becomes 1, fibMm2 becomes 0
    #     while fibM > 1:
    #
    #         # Check if fibMm2 is a valid location
    #         i = min(offset + fibMMm2, n - 1)
    #
    #         # If x is greater than the value at
    #         # index fibMm2, cut the subarray array
    #         # from offset to i
    #         if (arr[i] < x):
    #             fibM = fibMMm1
    #             fibMMm1 = fibMMm2
    #             fibMMm2 = fibM - fibMMm1
    #             offset = i
    #
    #             # If x is greater than the value at
    #         # index fibMm2, cut the subarray
    #         # after i+1
    #         elif (arr[i] > x):
    #             fibM = fibMMm2
    #             fibMMm1 = fibMMm1 - fibMMm2
    #             fibMMm2 = fibM - fibMMm1
    #
    #             # element found. return index
    #         else:
    #             return i
    #
    #             # comparing the last element with x */
    #     if fibMMm1 and arr[(offset + 1)] == x:
    #         return offset + 1
    #
    #         # element not found. return -1
    #     return -1


busca = SequencialSearch(1000, 40)  # Inicialzando o objeto
antes = time.time()
number = busca.sentry_sequence_search()
depois = time.time()  # Medindo o tempo

total = (depois - antes) * 1000
busca.plotting_graph(total)

print(number)
print("O tempo gasto foi: {:6f} mili-segundos". format(total))
