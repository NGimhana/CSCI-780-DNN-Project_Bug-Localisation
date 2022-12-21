import matplotlib.pyplot as plt
import numpy as np

def generate_map_graph(xMAPList, yMAPList):

    xData=xMAPList
    yData_MAP = yMAPList
    xData = np.array(xData)
    yData_Hit = np.array(yData_MAP)

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xData, yData_Hit, 'bo-', color='tab:blue' )

    # zip joins x and y coordinates in pairs
    for x,y in zip(xData,yData_Hit):

        label = "{:.2f}".format(y)

        plt.annotate(label,
                    (x,y), 
                    textcoords="offset points",
                    xytext=(0,10), 
                    ha='center') 

    ax.set_ylabel('MAP@K')
    ax.set_xlabel('K')
    ax.set_title("MAP@K")
    # display the plot
    plt.savefig('results/MAP.png')