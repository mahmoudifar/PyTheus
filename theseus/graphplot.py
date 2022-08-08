import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as collections
import theseus.theseus as th
import theseus.analyzer as anal 
import matplotlib.patheffects as pe

def drawEdge(edge, verts, ind, mult,ax, scale_max=None, max_thickness=10,
             show_val = False,fs = 15,markersize=25):
    colors = ['dodgerblue', 'firebrick', 'limegreen', 'darkorange', 'purple', 'yellow', 'cyan']
    col1 = colors[int(edge[2])]
    col2 = colors[int(edge[3])]

    vert1 = np.array(verts[int(edge[0])])
    vert2 = np.array(verts[int(edge[1])])
    if not np.array_equal(vert1, vert2):
        diff = vert1 - vert2
        rect = [diff[1], -diff[0]]
        rect /= np.linalg.norm(rect)
        hp = (vert1 + vert2) / 2 + (2 * ind - mult + 1) * 0.05 * rect
    else:
        hp = vert1 * 1.2

    if scale_max is None:
        lw = max_thickness

    else:
        lw = np.max([abs(max_thickness * edge[4]) / scale_max, 0.5])

    try:
        transparency = 0.2 + abs(edge[4]) * 0.8
        transparency =  min(transparency,1)
    except IndexError:
        transparency = 1
    
    ax.plot([vert1[0], hp[0]], [vert1[1], hp[1]], color=col1, linewidth=lw,alpha=transparency)
    ax.plot([hp[0], vert2[0]], [hp[1], vert2[1]], col2, linewidth=lw,alpha=transparency)

    if show_val:
        
        if transparency > 0.5 and col1 == "blue" :
            font_col = 'white'
        else: font_col = 'black'
        latex_weight = '${}$'.format(anal.num_in_str(edge[4])) 
        if latex_weight == '$$':
            latex_weight = '1'
        ax.text(np.mean([0.9*vert1[0], hp[0]]), np.mean([0.9*vert1[1], hp[1]]),
                latex_weight,
                bbox={'facecolor':col1 ,'alpha':transparency,'edgecolor':col2,'pad':1},c =font_col,
                ha='center', va='center',rotation=0,fontweight ='heavy',fontsize= fs)
    try:
        if edge[4] < 0:
            ax.plot(hp[0], hp[1], marker="d", markersize=markersize, markeredgewidth="3", markeredgecolor="black",
                     color="white")
    except:
        pass


def graphPlot(graph, scaled_weights=False, show=True, max_thickness=10,
              weight_product=False, ax_fig = (), add_title= '',
              show_value_for_each_edge= False, fontsize= 30,zorder=11,
              markersize=25):
    edge_dict = th.edgeBleach(graph.edges)

    num_vertices = len(np.unique(np.array(graph.edges)[:, :2]))

    angles = np.linspace(0, 2 * np.pi * (num_vertices - 1) / num_vertices, num_vertices)

    rad = 0.9
    vertcoords = []
    for angle in angles:
        x = rad * np.cos(angle)
        y = rad * np.sin(angle)
        vertcoords.append(tuple([x, y]))

    vertnums = list(range(num_vertices))
    verts = dict(zip(vertnums, vertcoords))

    if scaled_weights:
        try:
            scale_max = np.max(np.abs(np.array(graph.edges)[:, 4]))
        except:
            scale_max = None
    else:
        scale_max = None
    
    if len(ax_fig) == 0:
        fig, ax = plt.subplots(figsize=(10, 10))
    else: 
        fig, ax = ax_fig
    
    for uc_edge in edge_dict.keys():
        mult = len(edge_dict[uc_edge])
        for ii, coloring in enumerate(edge_dict[uc_edge]):
            drawEdge(uc_edge + coloring + tuple([graph[tuple(uc_edge + coloring)]]), verts, ii, mult,ax,
                     scale_max=scale_max, max_thickness=max_thickness,
                     show_val = show_value_for_each_edge,fs=0.8*fontsize,markersize=markersize)

    circ = []
    for vert, coords in verts.items(): 
        circ.append(plt.Circle(coords, 0.1, alpha=0.5))
        ax.text(coords[0], coords[1], str(vert), zorder=zorder,
                ha='center', va='center', size=fontsize)
        
    circ = collections.PatchCollection(circ, zorder=zorder-1)
    circ.set(facecolor='lightgrey',edgecolor='dimgray',linewidth=3)
    ax.add_collection(circ)

    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.axis('off')

    if weight_product:
        total_weight = np.product(graph.weights)
        
        wp = '${}$'.format(anal.num_in_str(total_weight) )
        if wp == '$$':
            wp = '1'
        ax.set_title( wp + str(add_title), fontsize=fontsize)
        
    if add_title != '' and weight_product is False :
        ax.set_title( str(add_title), fontsize=fontsize)
    
    if show:
        plt.show()
        plt.pause(0.01)
    else:
        pass
    return fig
