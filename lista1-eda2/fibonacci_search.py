import time
import matplotlib.pyplot as plt
# [0, 1, 1, 2, 3, 5, 8, 13...]
# return the fibonacci number at the index of n


def fill_vector_order(v):
    vector = list(range(0, v + 1))
    return vector


def fibonacci_generator(n):
    if n < 1:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_generator(n - 1) + fibonacci_generator(n - 2)

# return the index at which x exists inside arr
# return -1 otherwise


def fibonacci_search(arr, x):

    # find the smallest Fibonacci number greater than or equal
    # to the length of arr
    m = 0
    while fibonacci_generator(m) < len(arr): #
        m = m + 1

    # [10, 22, 30, 44, 56, 58, 60, 70, 100, 110, 130]
    # m = 7

    # m now contains the index of the the smallest Fibonacci
    # number greater than or equal to the length of the array
    # for example
    # if the length of arr is 11, FibonacciGenerator(m) should be 13

    # this is the length of that array from the
    # start that has been eliminated
    offset = -1

    # [10, 22, 30, 44, 56, 58, 60, 70, 100, 110, 130]
    # m = 7
    # offset = -1

    # make sure you fibonacci index is valid
    while fibonacci_generator(m) > 1:

        i = min( offset + fibonacci_generator(m - 2), len(arr) - 1)

        # [10, 22, 30, 44, 56, 58, 60, 70, 100, 110, 130]
        # m = 3
        # offset = 5
        # i = 6
        # x = 60

        if x > arr[i]:

            m = m - 1
            offset = i

        elif x < arr[i]:

            m = m - 2

        else:

            return "O elemento {} foi encontrado na posição {}".format(x, i)

    # this will run if there is one last element left
    if fibonacci_generator(m - 1) and arr[offset + 1] == x:
        return offset + 1

    # return -1 if the element doesn't exist in the array
    return "Não foi possível encontrar o elemento {}".format(x)


def plotting(t, array):
    new_time = int(round(t))
    x_vec = fill_vector_order(new_time)
    y_vec = array
    new_v = []
    for i in range(0, new_time + 1):
        new_v.append(y_vec[i])

    plt.plot(x_vec, new_v)
    plt.title('Search Method x Time')
    plt.xlabel('time x 100000')
    plt.ylabel('vector')
    plt.show()


# the search array
arr = [10, 22, 30, 44, 56, 58, 60, 70, 100, 110, 130]
x = 2

antes = time.time()
print(fibonacci_search(arr, x))
depois = time.time()
total = (depois - antes) * 100000
print("O tempo gasto foi: {:6f} mili-segundos". format(total))

plotting(total, arr)


