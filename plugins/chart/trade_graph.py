import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from plugins.bitquery.bitquery_7_day_trades import process_json
from millify import millify

# customise the plot
fig = plt.figure(figsize=(15, 15))
gs = fig.add_gridspec(1, 4)
ax1 = fig.add_subplot(gs[:, :-1])
ax2 = fig.add_subplot(gs[:, -1])

plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

def create_trade_graph():
    data_received = process_json()
    day = data_received['day_array'].astype(np.datetime64)
    tx_no = data_received['tx_number_array']
    buy_amt = data_received['buy_amount_array']
    sell_amt = data_received['sell_amount_array']
    tx_amt = data_received['tx_amount_array']

    N = len(day)
    space = np.arange(N)  # evenly spaced values
    width_bar = 0.2
    max_height = max(tx_amt)

    trade_bar = ax1.barh(space + width_bar * 2, tx_amt, height=width_bar, color='#7C83FD', edgecolor='white')
    buy_bar = ax1.barh(space + width_bar, buy_amt, height=width_bar, color='#54E346', edgecolor='white')
    sell_bar = ax1.barh(space, sell_amt, height=width_bar, color='#FF2442', edgecolor='white')

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height ( width when horizontal bar plots are used)
        """
        for rect in rects:
            width = rect.get_width()
            try:
                widthPlot = millify(width, precision=1)
            except:
                widthPlot = int(widthPlot)
            ax1.text(width + 0.04 * max_height, rect.get_y(),
                     '$%s' % widthPlot,
                     ha='center', va='bottom', rotation=0, fontsize=16)

    ax1.set_xlabel('Trade Amount', fontsize=20)
    ax1.set_ylabel('Date', fontsize=16)
    ax1.set_yticks(space + width_bar)  # equally spaced (im middle of bar-plot)
    ax1.set_yticklabels(day, rotation=0, fontsize=16)  # days are placed in middle of 3 bar-plots
    ax1.tick_params(axis='x', labelsize=16)

    ax1.legend((trade_bar, buy_bar, sell_bar), ('Total trades', 'Buy', 'Sell'))

    autolabel(trade_bar)
    autolabel(buy_bar)
    autolabel(sell_bar)

    linechart = ax2.plot(tx_no, space + width_bar, color='#F5D300', marker='o')
    ax2.set_xlabel('Number of Trades', fontsize=20)
    ax2.legend(linechart, '#trade')
    ax2.tick_params(labelleft=False, axis='x', labelsize=16)
    ax2.yaxis.set_ticklabels([])
    
    for i, txt in enumerate(tx_no):
        ax2.annotate(tx_no[i], xy=(tx_no[i], space[i] + width_bar), fontsize=12, xytext=(6, 0),
                     textcoords='offset points')

    # plt.show()

    bio = io.BytesIO()
    bio.name = "test.png"
    fig.savefig(bio, format='png', dpi=200)
    plt.close()  # important to free memory
    bio.seek(0)
    return bio

# create_trade_graph()
