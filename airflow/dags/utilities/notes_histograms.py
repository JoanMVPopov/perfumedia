import ast
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def get_histograms_for_notes(decade='All', gender='All', df=None, top_n=25,
                             current_dir=os.path.dirname(os.path.abspath(__file__)),
                             folder_name='temp'):

    notes = df['notes'].apply(lambda x: ast.literal_eval(x))

    dictionary_notes = dict()

    for note_list in notes:
        for current_note in note_list:
            if not dictionary_notes.get(current_note):
                dictionary_notes[current_note] = 1
            else:
                dictionary_notes[current_note] += 1

    num_unique_notes = len(dictionary_notes)
    n = top_n if num_unique_notes > top_n else num_unique_notes

    # select top n most frequently used notes (since it would not look nice if we displayed all notes)
    top_notes = sorted(dictionary_notes.items(), key=lambda x: x[1], reverse=True)[:n]

    notes = [item[0] for item in top_notes]
    values = [item[1] for item in top_notes]

    plt.figure(figsize=(16, 8))
    plt.bar(notes, values, color="#C96868")
    plt.xlabel('Notes')
    plt.ylabel('Number of perfumes')
    plt.title(f'Top {n} most frequently used notes')

    # force y-axis to display only rounded numbers
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    plt.subplots_adjust(bottom=0.25)  # Increase the bottom margin

    # add text below the x-axis label
    plt.figtext(0.5, 0.05, f'Total number of unique notes in dataset: {num_unique_notes}', ha='center', fontsize=14)

    # rotate ticks to reduce text overlap
    plt.xticks(rotation=45, ha="right", fontsize=8)

    file_name = f'{decade}_{gender}_notes_histogram.png'
    file_path_notes_histogram = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_notes_histogram, bbox_inches='tight')
