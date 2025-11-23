import plotext as plt

def plot_line(times, prices, title="Gráfico", y_label="Preço"):
    plt.clear_plot()
    plt.theme('dark')
    plt.plot(times, prices, marker='dot', color='cyan')
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel("Tempo")
    plt.canvas_color('black')
    plt.axes_color('black')
    plt.grid(True)
    plt.show()
