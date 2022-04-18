from csv import DictReader, DictWriter
from schemas import Vacancy

with open("vacancies2.csv", "r", newline="", encoding="utf-8") as f:
    reader = DictReader(f)
    with open("exp/noExperience.csv", "w", newline="") as f_noExperience:
        with open("exp/between1And3.csv", "w", newline="") as f_between1And3:
            with open("exp/between3And6.csv", "w", newline="") as f_between3And6:
                with open("exp/moreThan6.csv", "w", newline="") as f_moreThan6:
                    fieldnames = list(Vacancy.schema()["properties"].keys())
                    noExperience = DictWriter(f_noExperience, fieldnames)
                    between1And3 = DictWriter(f_between1And3, fieldnames)
                    between3And6 = DictWriter(f_between3And6, fieldnames)
                    moreThan6 = DictWriter(f_moreThan6, fieldnames)
                    noExperience.writeheader()
                    between1And3.writeheader()
                    between3And6.writeheader()
                    moreThan6.writeheader()
                    for row in reader:
                        match row.get("experience"):
                            case "Нет опыта":
                                noExperience.writerow(row)
                            case "От 1 года до 3 лет":
                                between1And3.writerow(row)
                            case "От 3 до 6 лет":
                                between3And6.writerow(row)
                            case "Более 6 лет":
                                moreThan6.writerow(row)

# {
#     "id": "noExperience",
#     "name": "Нет опыта"
# },
# {
#     "id": "between1And3",
#     "name": "От 1 года до 3 лет"
# },
# {
#     "id": "between3And6",
#     "name": "От 3 до 6 лет"
# },
# {
#     "id": "moreThan6",
#     "name": "Более 6 лет"
# }
