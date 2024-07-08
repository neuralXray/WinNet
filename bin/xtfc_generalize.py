def read_beta(n_neurons):
    beta = []
    time = []
    file = open('beta.txt', 'r')
    while True:
        line = file.readline()
        if not line:
            break
        time.append(float(line))
        betan = []
        for i in range(n_neurons):
            line = file.readline()
            elements = line.split(' ')
            nn_elements = []
            for element in elements:
                if element:
                    nn_elements.append(float(element))
            betan.append(nn_elements)
        beta.append(betan)
    file.close()
    return time, beta


def read_weight(n_neurons):
    file = open('weig.txt', 'r')
    weight = []
    bias = []
    for i in range(n_neurons):
        line = file.readline()
        elements = line.split(' ')
        nn_elements = []
        for element in elements:
            if element:
                nn_elements.append(float(element))
        weight.append(nn_elements[0])
        bias.append(nn_elements[1])
    file.close()
    return bias, weight


def predict(n, n_neurons, net_size, y0):
    from numpy import tanh, array, linspace, matmul, concatenate, log10
    x_i = 0
    x_f = 1
    time, beta = read_beta(n_neurons)
    bias, weight = read_weight(n_neurons)
    weight = array(weight).reshape(1, n_neurons)
    bias = array(bias).reshape(1, n_neurons)
    t_i = 0
    y0 = array(y0)
    times = []
    ys = []
    dys = []
    for i, step in enumerate(time[1:]):
        beta_c = array(beta[i])
        c = (x_f - x_i) / step
        x = linspace(x_i, x_f, n).reshape(n, 1)
        t = t_i + 1 / c * (x - x_i)
        times.append(t)
        g = tanh(matmul(x, weight) + bias) - tanh(bias)
        dg = (1 - tanh(matmul(x, weight) + bias)**2) * weight
        y = matmul(g, beta_c) + y0
        dy = c*matmul(dg, beta_c)
        ys.append(y)
        dys.append(dy)
        y0 = y[n - 1, :]
        t_i = t[-1]
    time = array(time)
    times = concatenate(times)
    ys = concatenate(ys)
    dys = concatenate(dys)
    return time, times, ys, dys


def plot(n, n_neurons, net_size, y0):
    import matplotlib.pyplot as plt
    time, times, ys, dys = predict(n, n_neurons, net_size, y0)
    fig, ax = plt.subplots(net_size, 2, sharex=True, figsize=(5, 9))
    for i in range(net_size):
        ax[i, 0].plot(times, ys[:, i], marker='.')
        #ax[i, 0].vlines(time, 0, max(ys[:, i]))
        ax[i, 1].plot(times, dys[:, i], marker='.')
        #ax[i, 1].vlines(time, 0, max(dys[:, i]))
    plt.xscale('log')
    plt.show()

