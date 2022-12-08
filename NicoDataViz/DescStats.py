'''
    Data Visualization module
    version: 1.0.1
'''

# Libraries
#---

# Numerical and data libraries
import numpy as np
import pandas as pd

# Graphs
from matplotlib import pyplot as plt
import seaborn as sns

class DescStats():
    # Attributes
    #---

    # Figure
    @property
    def fig(self):
        return self._fig

    # Subfigures
    @property
    def subfigs(self):
        return self._subfigs

    # Axes with the histograms
    @property
    def hist_axs(self):
        return self._hist_axs

    # Pyplot Histogram return
    @property
    def hist_ret(self):
        return self._hist_ret

    # Axes with the box and whisker plots
    @property
    def boxplot_axs(self):
        return self._boxplot_axs

    # Group of dataframes
    @property
    def group_dfs(self):
        return self._group_dfs

    # Titles
    @property
    def titles(self):
        return self._titles

    # Grid shape
    @property
    def grid_shape(self):
        return self._grid_shape

    # Titles
    @property
    def titles(self):
        return self._titles

    # Axes parameters
    @property
    def axes_params(self):
        return self._axes_params

    # Methods
    #---

    # Constructor
    def __init__(self, group_dfs, **kargs):
        # Group of dataframes
        self._group_dfs = group_dfs

        # Titles
        self._titles = {
            'plot_titles': False    # Use columns name as titles on plots
        }

        # Axes
        self._axes_params = {
            'share_all_x': False,
            'share_row_x': False,
            'share_col_x': False,
            'share_all_y': False,
            'share_row_y': False,
            'share_col_y': False,

        }

        # Arguments
        #---
        for key, value in kargs.items():
            # Titles
            if key in self.titles.keys():
                self.titles[key] = value

            # Axes
            if key in self.axes_params.keys():
                if isinstance(value, bool):
                    self.axes_params[key] = value

                else:
                    raise Exception('The %s attribute must be a string type' % key)

        # Build axes and figures
        self.__set_axes()

        # Build plots
        self.__set_plots()

        # Set style
        self.__set_style()

    # Build plots
    def __set_plots(self):
        # Histograms
        k = 0
        self._hist_ret = []

        for i in range(self.grid_shape[0]):
            for j in range(self._grid_shape[1]):
                data = self.group_dfs[i].iloc[:,j]

                # Histogram
                self._hist_ret.append(
                    self._hist_axs[k].hist(
                            data,
                            color = sns.color_palette()[j],
                            alpha = 0.7
                        )
                    )

                # Median
                self._hist_axs[k].axvline(
                        data.quantile(0.5),
                        color = 'dimgrey',
                        linestyle = '--'
                    )

                # Maximum frequency
                self._hist_axs[k].axhline(
                        max(self.hist_ret[-1][0]),
                        color = 'dimgrey',
                        linestyle = '--'
                    )

                # Counter
                k += 1

        # Box and Whisker Plots
        k = 0
        for i in range(self.grid_shape[0]):
            for j in range(self._grid_shape[1]):
                data = self.group_dfs[i].iloc[:,j]

                # Histogram
                self._boxplot_axs[k].boxplot(
                        data,
                        vert = False,
                        widths = 0.4,
                        medianprops = {
                            'color': sns.color_palette()[j],
                            'linewidth': 2
                        }
                    )

                # Titles
                if self.titles['plot_titles']:
                    self._boxplot_axs[k].set_title(
                            data.name,
                            fontsize = 14,
                            fontweight = 'bold',
                            pad = 20
                        )

                # Counter
                k += 1

    # Build axes and figures
    def __set_axes(self):
        # Grid shape
        self._grid_shape = np.zeros(2, dtype = 'int')
        self._grid_shape[0] = int(len(self.group_dfs))
        self._grid_shape[1] = int(np.max([df.shape[1] for df in self.group_dfs]))

        # Figure
        self._fig = plt.figure(figsize = (15, 2 + 3 * self.grid_shape[0]), dpi = 100)

        # Set subfigures
        self._subfigs = self.fig.subfigures(self.grid_shape[0], 1)
        if self.titles['plot_titles']:
            plt.subplots_adjust(bottom = 0.25)

        # GridSpecs
        for subfig in self._subfigs:
            gs = subfig.add_gridspec(nrows = 3, ncols = self.grid_shape[1], wspace = 0.20, hspace = 0)

        # Histograms
        #--
        self._hist_axs = []

        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                # Add plot structure
                self._hist_axs.append(self._subfigs[i].add_subplot(gs[1:, j]))

        # Boxplots
        #--
        self._boxplot_axs = []

        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                # Add plot structure
                self._boxplot_axs.append(self._subfigs[i].add_subplot(gs[0, j]))

    # Set axes limits
    def __set_axes_limits(self):
        self.__set_x_axes_limits()
        self.__set_y_axes_limits()

    # Set x-axes limits
    def __set_x_axes_limits(self):
        xlims = np.zeros((self.grid_shape[0], self.grid_shape[1], 2))

        # Share all x-axes
        if (self.axes_params['share_all_x'] == True) or ((self.axes_params['share_row_x'] == True) and (self.axes_params['share_col_x'] == True)):
            min_lim = min([df.min().min() for df in self.group_dfs])
            max_lim = max([df.max().max() for df in self.group_dfs])
            delta = max_lim - min_lim

            for i in range(self.grid_shape[0]):
                for j in range(self.grid_shape[1]):
                    xlims[i, j, 0] = min_lim - 0.1 * delta
                    xlims[i, j, 1] = max_lim + 0.1 * delta

        # Share x-axes in a row
        elif self.axes_params['share_row_x'] == True:
            for i in range(self.grid_shape[0]):
                min_lim = self.group_dfs[i].min().min()
                max_lim = self.group_dfs[i].max().max()
                delta = max_lim - min_lim

                for j in range(self.grid_shape[1]):
                    xlims[i, j, 0] = min_lim - 0.1 * delta
                    xlims[i, j, 1] = max_lim + 0.1 * delta

        # Share x-axes in a column
        elif self.axes_params['share_col_x'] == True:
            for j in range(self.grid_shape[1]):
                min_lim = min([df.iloc[:,j].min() for df in self.group_dfs])
                max_lim = max([df.iloc[:,j].max() for df in self.group_dfs])
                delta = max_lim - min_lim

                for i in range(self.grid_shape[0]):
                    xlims[i, j, 0] = min_lim - 0.1 * delta
                    xlims[i, j, 1] = max_lim + 0.1 * delta

        # Individual x-axes
        else:
            for i in range(self.grid_shape[0]):
                for j in range(self.grid_shape[1]):
                    data = self.group_dfs[i].iloc[:,j]
                    min_lim = data.min()
                    max_lim = data.max()
                    delta = max_lim - min_lim

                    xlims[i, j, 0] = min_lim - 0.1 * delta
                    xlims[i, j, 1] = max_lim + 0.1 * delta

        # Set limits
        k = 0
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                self._hist_axs[k].set_xlim(xlims[i, j])
                self._boxplot_axs[k].set_xlim(xlims[i, j])

                k += 1

    # Set y-axes limits
    def __set_y_axes_limits(self):
        ylims = np.zeros((self.grid_shape[0], self.grid_shape[1], 2))

        # Share all y-axes
        if (self.axes_params['share_all_y'] == True) or ((self.axes_params['share_row_y'] == True) and (self.axes_params['share_col_y'] == True)):
            max_lim = max([max(ret[0]) for ret in self.hist_ret])

            for i in range(self.grid_shape[0]):
                for j in range(self.grid_shape[1]):
                    ylims[i, j, 0] = 0
                    ylims[i, j, 1] = 1.1 * max_lim

        # Share y-axes in a row
        elif self.axes_params['share_row_y'] == True:
            for i in range(self.grid_shape[0]):
                max_lim = max([max(self.hist_ret[idx][0]) for idx in range(i * self.grid_shape[1], (i+1) * self.grid_shape[1])])

                for j in range(self.grid_shape[1]):
                    ylims[i, j, 0] = 0
                    ylims[i, j, 1] = 1.1 * max_lim

        # Individual x-axes
        else:
            k = 0
            for i in range(self.grid_shape[0]):
                for j in range(self.grid_shape[1]):
                    max_lim = max(self.hist_ret[k][0])

                    ylims[i, j, 0] = 0
                    ylims[i, j, 1] = 1.1 * max_lim

                    k += 1

        # Set limits
        k = 0
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                self._hist_axs[k].set_ylim(ylims[i, j])

                k += 1

    # Set appearance of plots
    def __set_style(self):
        # Theme
        plt.style.use('seaborn-ticks')

        # Style parameters
        plt.rcParams.update({
            'font.size': 14
        })

        # Limits
        self.__set_axes_limits()

        # Histograms
        #--
        k = 0
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                # Remove spines
                self._hist_axs[k].spines[['top', 'right']].set_visible(False)

                # Ticks
                #---
                self._hist_axs[k].yaxis.set_tick_params(width = 1.5)
                self._hist_axs[k].xaxis.set_tick_params(width = 1.5)

                # X ticks
                data = self.group_dfs[i].iloc[:,j]
                self._hist_axs[k].set_xticks([
                        data.min(),
                        data.quantile(0.5),
                        data.max()
                    ])

                # Y ticks
                data = self.hist_ret[k][0]
                self._hist_axs[k].set_yticks([
                        0,
                        max(data) / 2,
                        max(data)
                    ])

                k += 1

        # Boxplots
        #--
        k = 0
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                # Remove spines
                self._boxplot_axs[k].spines[['bottom', 'left', 'right']].set_visible(False)
                self._boxplot_axs[k].xaxis.tick_top()

                # Remove ticks
                self._boxplot_axs[k].yaxis.set_tick_params(left = False, labelleft = False, width = 1.5)
                self._boxplot_axs[k].xaxis.set_tick_params(bottom = False, labelbottom = False, width = 1.5)

                # X ticks - Boxplot
                data = self.group_dfs[i].iloc[:,j]
                self._boxplot_axs[k].set_xticks([
                        data.quantile(0.25),
                        data.quantile(0.75)
                    ])

                k += 1

    # Show plots
    def show_plots(self):
        self.fig.show()


    # Save figure
    def save(self):
        self.fig.savefig(
                'graphs/desc_stats.png',
                dpi = 100,
                format = 'png',
                transparent = False,
                bbox_inches = 'tight'
             )
