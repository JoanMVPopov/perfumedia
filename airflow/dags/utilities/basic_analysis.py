import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os

# TODO: Implement try-except clauses


def calculate_basic_stats_and_diagrams(decade='All', gender='All', df=None,
                                       current_dir=os.path.dirname(os.path.abspath(__file__)),
                                       folder_name='temp'):

    df_filtered_rubrics_only = df[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']]

    get_basic_table_stats(decade, gender, df_filtered_rubrics_only,
                          current_dir, folder_name)

    get_boxplots(decade, gender, df_filtered_rubrics_only,
                 current_dir, folder_name)

    get_qq_plots(decade, gender, df_filtered_rubrics_only,
                 current_dir, folder_name)

    get_pairplot(decade, gender, df_filtered_rubrics_only,
                 current_dir, folder_name)

    get_violin_plots(decade, gender, df_filtered_rubrics_only,
                     current_dir, folder_name)


def get_basic_table_stats(decade='All', gender='All', df=None,
                          current_dir=os.path.dirname(os.path.abspath(__file__)),
                          folder_name='temp'):

    summary = df.describe()
    median = df.median()
    # if multiple modes, select first one
    mode = df.mode().iloc[0]

    summary_transposed = summary.T  # Transpose summary statistics
    summary_transposed['median'] = median
    summary_transposed['mode'] = mode

    # split the table into two parts
    columns_part1 = ['count', 'mean', 'median', 'mode', 'std']
    columns_part2 = ['25%', '50%', '75%', 'min', 'max', ]

    fig, axes = plt.subplots(2, 1, figsize=(5, 5))

    # First part of the table
    axes[0].axis('off')
    part1_table = axes[0].table(
        cellText=summary_transposed[columns_part1].round(2).values,
        rowLabels=summary_transposed.index,
        colLabels=columns_part1,
        loc='center'
    )

    # Second part of the table
    axes[1].axis('off')
    part2_table = axes[1].table(
        cellText=summary_transposed[columns_part2].round(2).values,
        rowLabels=summary_transposed.index,
        colLabels=columns_part2,
        loc='center'
    )

    for table in [part1_table, part2_table]:
        table.auto_set_font_size(False)
        table.set_fontsize(10)

    plt.tight_layout()

    file_name = f'{decade}_{gender}.png'
    file_path_save_table = os.path.join(current_dir, folder_name, file_name)

    plt.savefig(file_path_save_table, bbox_inches='tight')


def get_boxplots(decade='All', gender='All', df=None,
                 current_dir=os.path.dirname(os.path.abspath(__file__)),
                 folder_name='temp'):

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df)
    plt.title("Box Plots of Ratings")

    file_name = f'{decade}_{gender}_box_plots.png'
    file_path_box_plots = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_box_plots, bbox_inches='tight')


def get_qq_plots(decade='All', gender='All', df=None,
                 current_dir=os.path.dirname(os.path.abspath(__file__)),
                 folder_name='temp'):

    fig, axes = plt.subplots(len(df.columns), 1, figsize=(6, 14))
    for i, col in enumerate(df.columns):
        stats.probplot(df[col], dist="norm", plot=axes[i])
        axes[i].set_title(f"QQ Plot for {col}")
        axes[i].set_xlabel("Ordered value quantiles")
        axes[i].set_xlabel("Normal quantiles")
    plt.tight_layout()

    file_name = f'{decade}_{gender}_qq_plots.png'
    file_path_qq_plots = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_qq_plots, bbox_inches='tight')


def get_pairplot(decade='All', gender='All', df=None,
                 current_dir=os.path.dirname(os.path.abspath(__file__)),
                 folder_name='temp'):

    g = sns.pairplot(df, corner=True, diag_kind=None)

    # replace diagonal elements with custom histograms
    for i in range(len(df.columns)):
        ax = g.axes[i, i]
        if ax is not None:  # check if the axis exists
            g.fig.delaxes(ax)  # remove the existing axis
            new_ax = g.fig.add_subplot(len(df.columns), len(df.columns),
                                       i * len(df.columns) + i + 1)

            ax = sns.histplot(df.iloc[:, i], bins=15, kde=False, ax=new_ax,
                              color="skyblue")  # add histogram
            ax.set_title(f"Histogram of {df.columns[i]}", fontsize=10,
                         fontweight='bold')

    g.fig.subplots_adjust(hspace=0.5, wspace=0.5)

    file_name = f'{decade}_{gender}_pairplots.png'
    file_path_pairplots = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_pairplots, bbox_inches='tight')


def get_violin_plots(decade='All', gender='All', df=None,
                     current_dir=os.path.dirname(os.path.abspath(__file__)),
                     folder_name='temp'):

    plt.figure(figsize=(8, 6))
    sns.violinplot(data=df)
    plt.title("Violin Plots of Ratings")

    file_name = f'{decade}_{gender}_violin_plots.png'
    file_path_violin_plots = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_violin_plots, bbox_inches='tight')
