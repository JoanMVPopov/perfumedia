import gc
import json
import tracemalloc

import torch

from backend.etl.utils.ModelSingleton import Model


def streaming_inference_generator(query, data, model, number_of_perfumes, step):
    try:
        all_ranks = []

        for i in range(0, number_of_perfumes, step):
            chunk_data = data['generated_descriptions'][i:i + step].copy()
            current_ranks = model.calculate_similarity(query, chunk_data)

            all_ranks.extend(current_ranks)

            # Clean up chunk
            del chunk_data
            print("+++++++++++")
            #print(torch.cuda.memory_summary())
            print("+++++++++++")
            torch.cuda.empty_cache()  # Free GPU cache
            gc.collect()

            processed = min(i + step, number_of_perfumes)
            progress_percent = round((processed / number_of_perfumes) * 100, 2)

            yield f"data: {json.dumps({'progress': progress_percent})}\n\n"

        sorted_all_ranks = sorted(all_ranks, key=lambda x: x['score'], reverse=True)
        if sorted_all_ranks and sorted_all_ranks[0]['score'] <= 0:
            sorted_all_ranks = sorted_all_ranks[::-1]

        top_20_indices = [rank['corpus_id'] for rank in sorted_all_ranks[:20]]

        # Get only needed data for final results
        similarities = []
        for index, i in enumerate(top_20_indices):
            row = data.iloc[i]
            similarities.append({
                "link": row["link"],
                "description": row["description"],
                "image": row["image"],
                "similarity": -index,
                "scent": row['scent'],
                "longevity": row['longevity'],
                "sillage": row['sillage'],
                "bottle": row['bottle'],
                "value_for_money": row['value_for_money']
            })

        yield f"data: {json.dumps({'final': similarities})}\n\n"
    except Exception as e:
        print("Err In streamingModeSimilarity.py")
        print(e)
    finally:
        print("Deleting stuff...")
        del query, data, model, number_of_perfumes, step
        torch.cuda.empty_cache()
        gc.collect()
