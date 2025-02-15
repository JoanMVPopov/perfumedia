import ast
import random


def generateDescriptions(data, categories, ratings):

    generated_descriptions = []

    for i in range(len(data)):
        current_data = data.iloc[i]
        brand = current_data['brand']
        decade = str(current_data['rel_decade']) + 's'
        notes = ", ".join(current_data['notes'])

        scent_profile = ""
        gender_profile = ""
        season_profile = ""
        occasion_profile = ""

        for category in categories:
            current_category = current_data[category]
            current_category_numbers = current_data[f"{category}_numbers"]
            zipped = zip(current_category, current_category_numbers)

            if category == 'type':
                sorted_zip = [v[0] for v in sorted(zipped, key=lambda x: x[1], reverse=True)]
                scent_profile = ", ".join(sorted_zip[0:4]) if len(sorted_zip) > 4 else ", ".join(
                    sorted_zip[0:len(sorted_zip)])
            elif category == 'style':
                masculine_value = None
                feminine_value = None
                for value in zipped:
                    if value[0] == 'Masculine':
                        masculine_value = value[1]
                    elif value[0] == 'Feminine':
                        feminine_value = value[1]

                if masculine_value is None and feminine_value is None:
                    gender_profile = "Unisex"
                elif masculine_value is not None:
                    if feminine_value is not None:
                        if abs(feminine_value - masculine_value) < 10:
                            gender_profile = "Unisex"
                        elif feminine_value > masculine_value:
                            gender_profile = "Feminine"
                        else:
                            gender_profile = "Masculine"
                    else:
                        gender_profile = "Masculine"
                else:
                    gender_profile = "Feminine"
            elif category == 'season':
                for value in zipped:
                    if value[1] >= 20.0:
                        season_profile += value[0] + ", "

                # remove trailing comma and white space
                if len(season_profile) > 2:
                    season_profile = season_profile[0: len(season_profile) - 2]
            else:
                for value in zipped:
                    if value[1] >= 20.0:
                        occasion_profile += value[0] + ", "

                # remove trailing comma and white space
                if len(occasion_profile) > 2:
                    occasion_profile = occasion_profile[0: len(occasion_profile) - 2]

        ratings_grades = []
        for rating in ratings:
            if current_data[rating] < 5.0:
                ratings_grades.append("bad")
            elif 5.0 <= current_data[rating] < 6.0:
                ratings_grades.append("alright")
            elif 6.0 <= current_data[rating] < 7.5:
                ratings_grades.append("good")
            elif 7.5 <= current_data[rating] < 8.5:
                ratings_grades.append("very good")
            elif current_data[rating] >= 8.5:
                ratings_grades.append("amazing")

        scent = ratings_grades[0]
        longevity = ratings_grades[1]
        sillage = ratings_grades[2]
        bottle = ratings_grades[3]
        value = ratings_grades[4]

        sentence_1 = f"The brand of this perfume is {brand}, and it was released in the {decade}. ".lower()
        sentence_2 = f"The notes of this perfume are {notes}. ".lower()
        sentence_3 = f"The scent profile of this perfume is {scent_profile}. ".lower()
        sentence_4 = f"The gender profile of this perfume is {gender_profile}. ".lower()
        sentence_5 = f"Suitable seasons for this perfume are {season_profile}. ".lower()
        sentence_6 = f"The perfume is primarily for {occasion_profile} use. ".lower()
        sentence_7 = (
            f"The scent of this perfume is {scent}, the longevity is {longevity}, the sillage is {sillage}, the bottle "
            f"design is {bottle}, value for money is {value}. ").lower()

        sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6, sentence_7]

        random.shuffle(sentences)

        description = "".join(sentences)

        generated_descriptions.append(description)

    data['generated_descriptions'] = generated_descriptions
