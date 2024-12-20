import ast
import os

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def calculate_correlation_and_graphs(decade='All', gender='All', df=None, top_n=50,
                                     categories=None,
                                     current_dir=os.path.dirname(os.path.abspath(__file__)),
                                     folder_name='temp'):
    # flatten the notes column into binary columns
    df['notes'] = df['notes'].apply(lambda x: ast.literal_eval(x))
    notes_dummies = df['notes'].explode().str.get_dummies().groupby(level=0).max()

    # get the top n most frequent notes
    n = top_n
    note_counts = df['notes'].explode().value_counts()
    top_notes = note_counts.head(n).index

    # filter the notes dummies to include only the top n notes
    notes_dummies_top = notes_dummies[top_notes]

    # CORRELATION (notes - rubrics)
    get_corr_notes_rubrics(decade, gender, df, top_n,
                           notes_dummies_top, current_dir, folder_name)

    # CORRELATION (notes - categories)
    df_encoded_categories = get_corr_notes_categories(decade, gender, df, top_n, categories,
                                                      notes_dummies_top, current_dir, folder_name)

    # CORRELATION (categories - rubrics)
    get_corr_categories_rubrics(decade, gender, df, top_n, df_encoded_categories,
                                current_dir, folder_name)


def get_corr_notes_rubrics(decade='All', gender='All', df=None, n=50,
                           notes_dummies_top=None,
                           current_dir=os.path.dirname(os.path.abspath(__file__)),
                           folder_name='temp'):
    # combine the binary top notes columns with the rubrics
    df_combined = pd.concat([notes_dummies_top, df[['scent', 'longevity', 'sillage', 'value_for_money']]],
                            axis=1)
    correlation_matrix = df_combined.corr()

    # display correlations between top notes and rubrics
    note_columns = notes_dummies_top.columns
    rubric_columns = ['scent', 'longevity', 'sillage', 'value_for_money']

    correlation_notes_rubrics = correlation_matrix.loc[note_columns, rubric_columns]

    plt.figure(figsize=(18, 16))
    sns.heatmap(correlation_notes_rubrics, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title(f"Correlation Between Top {n} Notes and Rubrics")

    plt.tight_layout()
    file_name = f'{decade}_{gender}_notes_rubrics_correlation.png'
    file_path_notes_rubrics_correlation = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_notes_rubrics_correlation, bbox_inches='tight')


def get_corr_notes_categories(decade='All', gender='All', df=None, n=50,
                              categories=None,
                              notes_dummies_top=None,
                              current_dir=os.path.dirname(os.path.abspath(__file__)),
                              folder_name='temp'):
    df_encoded_categories = pd.DataFrame()

    for category in categories:
        df_type = df[category].apply(lambda x: ast.literal_eval(x))
        df_type_nums = df[f'{category}_numbers'].apply(lambda x: ast.literal_eval(x))

        dictionary = dict()

        for i, type_list in enumerate(df_type):
            for j, specific_type in enumerate(type_list):
                prefill_list = None
                dict_val = dictionary.get(specific_type)

                if not dict_val:
                    prefill_list = [0] * len(df_type)
                else:
                    prefill_list = dict_val

                prefill_list[i] = df_type_nums.iloc[i][j]
                dictionary[specific_type] = prefill_list

        df_encoded_categories = pd.concat(
            [df_encoded_categories, pd.DataFrame(dictionary)], axis=1
        )

    df_combined = pd.concat(
        [notes_dummies_top, df_encoded_categories],
        axis=1)

    correlation_matrix = df_combined.corr()

    # display correlations between top notes and rubrics
    note_columns = notes_dummies_top.columns
    category_columns = df_encoded_categories.columns

    correlation_notes_categories = correlation_matrix.loc[note_columns, category_columns]

    plt.figure(figsize=(18, 16))
    sns.heatmap(correlation_notes_categories, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title(f"Correlation Between Top {n} Notes and Categories")

    plt.tight_layout()
    file_name = f'{decade}_{gender}_notes_categories_correlation.png'
    file_path_notes_categories_correlation = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_notes_categories_correlation, bbox_inches='tight')

    # needed for last correlation method (otherwise need to recalculate)
    return df_encoded_categories


def get_corr_categories_rubrics(decade='All', gender='All', df=None, n=50,
                                df_encoded_categories=None,
                                current_dir=os.path.dirname(os.path.abspath(__file__)),
                                folder_name='temp'):
    df_combined = pd.concat(
        [df_encoded_categories, df[['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']]],
        axis=1)

    correlation_matrix = df_combined.corr()

    rubric_columns = ['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']
    category_columns = df_encoded_categories.columns

    correlation_categories_rubrics = correlation_matrix.loc[category_columns, rubric_columns]

    plt.figure(figsize=(18, 16))
    sns.heatmap(correlation_categories_rubrics, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title(f"Correlation Between Top {n} Notes and Categories")

    plt.tight_layout()
    file_name = f'{decade}_{gender}_categories_rubrics_correlation.png'
    file_path_notes_categories_correlation = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_notes_categories_correlation, bbox_inches='tight')
