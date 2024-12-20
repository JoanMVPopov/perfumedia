import os

from matplotlib import pyplot as plt


def calculate_rubric_progression_throughout_decades(decade='All', gender='All', df=None,
                                                    current_dir=os.path.dirname(os.path.abspath(__file__)),
                                                    folder_name='temp'):
    # reset index otherwise rel_year becomes index
    # selects all 5 rubric columns + years and excludes everything else
    df_agg = df.groupby('rel_year')[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']].agg(
        ['mean', 'std']).reset_index()

    # if year has only 1 record, std will be NaN and the graph will look funny
    df_agg.fillna(0.1, inplace=True)

    fig, axs = plt.subplots(5, 1, figsize=(12, 30))

    # range 5 because of 5 rubrics
    for i in range(5):
        axs[i].plot(df_agg.iloc[:, 0], df_agg.iloc[:, 2 * i + 1], label='Mean Value', color='#C96868',
                    linewidth=2, marker='o')

        # adding the shaded region for std
        axs[i].fill_between(df_agg.iloc[:, 0],
                            df_agg.iloc[:, 2 * i + 1] - df_agg.iloc[:, 2 * i + 2],
                            df_agg.iloc[:, 2 * i + 1] + df_agg.iloc[:, 2 * i + 2],
                            color='#FFF4EA', alpha=1, label='±1 Std. Dev.')

        axs[i].set_title(f'Yearly Averages with Standard Deviation for {df_agg.columns[2 * i + 1][0]}', fontsize=16)
        axs[i].set_xlabel('Year', fontsize=12)
        axs[i].set_ylabel('Average Value', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.3)

    plt.tight_layout()

    file_name = f'{decade}_{gender}_avg_rubric_progression.png'
    file_path_rubric_progression = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_rubric_progression, bbox_inches='tight')
