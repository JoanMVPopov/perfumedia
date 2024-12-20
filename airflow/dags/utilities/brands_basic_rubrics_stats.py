import os

from matplotlib import pyplot as plt


def calculate_basic_brand_rubric_stats_table(decade='All', gender='All', df=None, top_n=10,
                                             current_dir=os.path.dirname(os.path.abspath(__file__)),
                                             folder_name='temp'):
    # Aggregation step
    df_brands_agg = df.groupby('brand')[
        ['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']].agg(['mean'])
    df_counts = df.groupby('brand').size().reset_index(name='count')

    # Flatten the MultiIndex for column labels in df_brands_agg
    df_brands_agg.columns = [col[0] if isinstance(col, tuple) else col for col in df_brands_agg.columns]

    # Merge counts with aggregated data
    df_brands_agg = df_counts.merge(df_brands_agg, on='brand')

    # Select the top n based on count
    n = len(df_brands_agg) if (len(df_brands_agg) <= 10) else top_n
    df_brands_agg = df_brands_agg.sort_values('count', ascending=False).head(n)

    df_brands_agg.reset_index(inplace=True, drop=True)

    # Add note for superscript meaning
    note = "Colored cells indicate highest value in column"

    # Create the table
    plt.figure(figsize=(10, 6))
    current_table = plt.table(
        cellText=df_brands_agg.iloc[:, 1:].values.round(2),
        rowLabels=df_brands_agg.iloc[:, 0].values,
        colLabels=df_brands_agg.columns[1:],
        loc='center'
    )

    for i, row in df_brands_agg.iterrows():
        for j, col in enumerate(df_brands_agg.columns[1:]):
            is_max = row[col] == df_brands_agg[col].max() if col != 'count' else False
            if is_max:
                cell = current_table.get_celld()[i + 1, j]  # +1 for header row
                cell.set_facecolor('#C96868')

    # Add a note below the table
    plt.text(0.5, 0.01, note, ha='center', fontsize=10)

    # Adjust font size
    current_table.auto_set_font_size(True)
    #current_table.set_fontsize(10)

    # Hide the axes
    plt.axis('off')

    plt.tight_layout()
    file_name = f'{decade}_{gender}_brands_stats.png'
    file_path_brands_stats = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_brands_stats, bbox_inches='tight')
