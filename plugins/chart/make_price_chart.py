import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import deque
import random
import time
import matplotlib
from plugins.timefrom import display_time

matplotlib.use('Agg')



# customization
plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
]


def create_price_graph(data):
    x_data = data[:, 0]
    # x_data = np.array(data[:, 0]).astype(np.float)
    y_data = np.array(data[:, 1]).astype(np.float)

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    # x axis format as date ( x_label in HH:MM format)
    myFmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(myFmt)


    ##########################################################################################
    ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

    color = random.choice(colors)
    ax.plot(x_data, y_data, color=color)

    # make lines glow
    lines = ax.get_lines()

    n_glow_lines = 10
    diff_linewidth = 1.05
    alpha_value = 0.3 / n_glow_lines

    for line in lines:
        data = line.get_data()
        linewidth = line.get_linewidth()
        try:
            step_type = line.get_drawstyle().split('-')[1]
        except:
            step_type = None

        for n in range(1, n_glow_lines + 1):
            if step_type:
                glow_line, = ax.step(*data)
            else:
                glow_line, = ax.plot(*data)
            glow_line.update_from(line)

            glow_line.set_alpha(alpha_value)
            glow_line.set_linewidth(linewidth + (diff_linewidth * n))
            glow_line.is_glow_line = True  # mark the glow lines, to disregard them in the underglow function.

    # underflow

    # because ax.fill_between changes axis limits, save current xy-limits to restore them later:
    xlims, ylims = ax.get_xlim(), ax.get_ylim()
    alpha_underglow = 0.1
    for line in lines:
        # don't add underglow for glow effect lines:
        if hasattr(line, 'is_glow_line') and line.is_glow_line:
            continue
        x, y = line.get_data()
        color = line.get_c()

        try:
            step_type = line.get_drawstyle().split('-')[1]
        except:
            step_type = None

        ax.fill_between(x=x,
                        y1=y,
                        y2=[0] * len(y),
                        color=color,
                        step=step_type,
                        alpha=alpha_underglow)

    ax.set(xlim=xlims, ylim=ylims)

    #############################################################################

    ax.yaxis.set_ticks_position("right")
    ax.get_yaxis().get_major_formatter().set_useOffset(False)  # remove scientific notation

    # ax.set_xlabel('x')
    ax.set_ylabel('Price (USD)')
    ax.set_title(f'Token chart (since {display_time(int(abs(x_data[0].timestamp() - x_data[-1].timestamp())))})'
                 ,fontsize=18)
    # plt.show()

    bio = io.BytesIO()
    bio.name = "test.png"
    fig.savefig(bio, format='png', dpi=70, bbox_inches='tight')
    plt.close()  # important to free memory
    bio.seek(0)
    return bio