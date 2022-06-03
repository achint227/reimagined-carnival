import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


def plot_figure3d(n):
    axes=[]
    x = n**0.5
    r, c = [int(val) for val in [np.round(x), np.ceil(x)]]
    print(r,c)
    fig = plt.figure(figsize=(10*c,10*r))
    for i in range(n):
        axes.append(fig.add_subplot(r,c,i+1, projection='3d'))
    return fig, axes     

def composite_plot3d(data,x_axis: str, yz_pairs: list, plot_type: str = 'scatter'):
    n = len(yz_pairs)
    fig, axes = plot_figure3d(n)
    for i in range(n):
        y_axis=yz_pairs[i][0]
        z_axis=yz_pairs[i][1]
        y=data[y_axis]
        z=data[z_axis]
        x=data[x_axis]
        if plot_type=='scatter':
            axes[i].scatter(x,y,z,c=z)
        elif plot_type=='bar':
            axes[i].bar3d(x=x,y=y,z=np.zeros_like(z),dx=np.ones_like(x),dy=np.ones_like(y),dz=z,color='green')
        else:
            axes[i]
        
        axes[i].set_xlabel(x_axis)
        axes[i].set_ylabel(y_axis)
        axes[i].set_zlabel(z_axis)
    return fig    
        