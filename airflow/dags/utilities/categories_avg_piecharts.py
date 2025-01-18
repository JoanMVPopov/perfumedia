import ast
import os
import matplotlib.pyplot as plt


def get_avg_categories_piecharts(decade='All', gender='All', df=None, threshold=1,
                                 categories=None,
                                 current_dir=os.path.dirname(os.path.abspath(__file__)),
                                 folder_name='temp',
                                 filename_custom=None):

    fig, axs = plt.subplots(4, 1, figsize=(12, 36))

    for i, category in enumerate(categories):
        dictionary = get_category_avg_pie_chart(df, category, threshold)

        # create a pie chart from the dictionary values
        labels = dictionary.keys()
        sizes = dictionary.values()

        axs[i].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        axs[i].set_title(f'Pie Chart of average {category} values')

        if 'Others' in dictionary:
            fig.text(0.5, 0.01, f'"Others" includes categories below the threshold of {threshold}% per pie',
                     ha='center', fontsize=10, color='gray')

    plt.tight_layout()
    file_name = f'{decade}_{gender}_avg_categories_piecharts.png' if filename_custom is None else filename_custom
    file_path_categories_piecharts = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_categories_piecharts, bbox_inches='tight')
    plt.close(fig)


def get_category_avg_pie_chart(df, category='type', threshold=1):
    categories = df[category].apply(lambda x: ast.literal_eval(x))
    numbers = df[f'{category}_numbers'].apply(lambda x: ast.literal_eval(x))

    dictionary = dict()

    for i, category_list in enumerate(categories):
        for j, category_j in enumerate(category_list):
            # if falsy value (still not in dictionary)
            if not dictionary.get(category_j):
                dictionary[category_j] = numbers.iloc[i][j]
            else:
                dictionary[category_j] += numbers.iloc[i][j]

    # get the average per category
    avg_dict = {key: (value / len(categories)) for key, value in dictionary.items()}

    filtered_dict = {}
    small_value_sum = 0

    for key, value in avg_dict.items():
        if value < threshold:
            small_value_sum += value  # Add small values to 'Others'
        else:
            filtered_dict[key] = value

    if small_value_sum > 0:
        filtered_dict['Others'] = small_value_sum

    return filtered_dict
