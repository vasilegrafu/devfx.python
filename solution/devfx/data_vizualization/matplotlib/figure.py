import matplotlib as mpl
import matplotlib.pyplot
import matplotlib.gridspec
import matplotlib.animation
import devfx.reflection as refl
from .figuregrid import FigureGrid
from .figures import Figures

class Figure(object):
    def __init__(self, size=(8, 4), dpi=None,
                       grid=(1, 1),
                       facecolor=None,
                       linewidth=0.0, edgecolor=None, frameon=True):
        self.__figure = mpl.pyplot.figure(figsize=size, dpi=dpi,
                                          facecolor=facecolor,
                                          linewidth=linewidth, edgecolor=edgecolor, frameon=frameon)
        if(grid is None):
            self.__grid = None
        else:
            self.__grid = FigureGrid(*grid)

        self.__animation = None

    """----------------------------------------------------------------
    """
    def __getitem__(self, position):
        return self.__grid[position]

    """------------------------------------------------------------------------------------------------
    """ 
    def new_chart2d(self, position=None):
        if(position is None):
            position=(1, 1, 1)
            return self.__figure.add_subplot(*position)
        elif(refl.is_typeof(position, mpl.gridspec.SubplotSpec)):
            return self.__figure.add_subplot(position)
        elif(refl.is_typeof(position, int)):
            return self.__figure.add_subplot(position)
        else:
            if(len(position) == 3 and all([not refl.is_iterable(_) for _ in position])):
                return self.__figure.add_subplot(*position)
            if(len(position) == 3 and all([refl.is_iterable(_) for _ in position])):
                return mpl.pyplot.subplot2grid(position[0], position[1], rowspan = position[2][0], colspan = position[2][1])

    """------------------------------------------------------------------------------------------------
    """         
    def new_chart3d(self, position=None):
        if(position is None):
            position=(1, 1, 1)
            return self.__figure.add_subplot(*position, projection='3d')
        elif(refl.is_typeof(position, mpl.gridspec.SubplotSpec)):
            return self.__figure.add_subplot(position, projection='3d')
        elif(refl.is_typeof(position, int)):
            return self.__figure.add_subplot(position, projection='3d')
        else:
            if(len(position) == 3 and all([not refl.is_iterable(_) for _ in position])):
                return self.__figure.add_subplot(*position, projection='3d')
            if(len(position) == 3 and all([refl.is_iterable(_) for _ in position])):
                return mpl.pyplot.subplot2grid(position[0], position[1], rowspan = position[2][0], colspan = position[2][1], projection='3d')

    """------------------------------------------------------------------------------------------------
    """         
    def new_chartPolar(self, position=None):
        if(position is None):
            position=(1, 1, 1)
            return self.__figure.add_subplot(*position, projection='polar')
        elif(refl.is_typeof(position, mpl.gridspec.SubplotSpec)):
            return self.__figure.add_subplot(position, projection='polar')
        elif(refl.is_typeof(position, int)):
            return self.__figure.add_subplot(position)
        else:
            if(len(position) == 3 and all([not refl.is_iterable(_) for _ in position])):
                return self.__figure.add_subplot(*position, projection='polar')
            if(len(position) == 3 and all([refl.is_iterable(_) for _ in position])):
                return mpl.pyplot.subplot2grid(position[0], position[1], rowspan = position[2][0], colspan = position[2][1], projection='polar')

    """------------------------------------------------------------------------------------------------
    """
    def show(self, block=True):
        Figures.show(figure=self.__figure, block=block)

    def refresh(self):
        self.__figure.canvas.update()
        self.__figure.canvas.draw()
        self.__figure.canvas.flush_events()

    def clear(self, chart=None):
        if (chart is not None):
            chart.axes.clear()
        else:
            for axes in self.__figure.get_axes():
                axes.clear()

    def clear_data(self, chart=None):
        if (chart is not None):
            chart.axes.lines = []
            chart.axes.patches = []
            chart.axes.collections = []
            chart.axes.images = []
        else:
            for axes in self.__figure.get_axes():
                axes.lines = []
                axes.patches = []
                axes.collections = []
                axes.images = []

    def empty(self, chart=None):
        if (chart is not None):
            self.__figure.delaxes(chart.axes)
        else:
            for axes in self.__figure.get_axes():
                self.__figure.delaxes(axes)

    def close(self):
        Figures.close(figure=self.__figure)

    """------------------------------------------------------------------------------------------------
    """     
    def animation_fn(self, init_fn=None, fn=None, fn_args=None, frames=None, interval=256):
        self.__animation = mpl.animation.FuncAnimation(self.__figure, init_func=init_fn, func=fn, fargs=fn_args, frames=frames, interval=interval)
        return self.__animation