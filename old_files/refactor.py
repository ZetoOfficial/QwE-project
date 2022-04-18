import csv
from collections import Counter

data = []

# with open("./vacancies3.csv", "r", newline="") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         area_json_data = (
#             row.get("area", "2")
#             .replace("'", '"')
#             .replace("None", "null")
#             .replace("False", "false")
#             .replace("True", "true")
#         ) or '{"name": "Не указан"}'
#         salary_json_data = (
#             row.get("salary", "2")
#             .replace("'", '"')
#             .replace("None", "null")
#             .replace("False", "false")
#             .replace("True", "true")
#         ) or '{"from": 0, "to": 0, "currency": "RUR"}'
#         key_skills_json_data = (
#             row.get("key_skills", "2")
#             .replace("'", '"')
#             .replace("None", "null")
#             .replace("False", "false")
#             .replace("True", "true")
#         ) or "[]"
#         experience_json_data = (
#             row.get("experience", "2")
#             .replace("'", '"')
#             .replace("None", "null")
#             .replace("False", "false")
#             .replace("True", "true")
#         ) or "[]"
#         area_json_data = json.loads(area_json_data)
#         salary_json_data = json.loads(salary_json_data)
#         key_skills_json_data = json.loads(key_skills_json_data)
#         experience_json_data = json.loads(experience_json_data)

#         # id,name,area,salary,experience,description,key_skills,alternate_url
#         # key_skills = json.loads(row.get("key_skills", "[]"))
#         key_skills = ", ".join([skill.get("name") for skill in key_skills_json_data])
#         experience = experience_json_data.get("name")
#         print(
#             type(salary_json_data.get("from", 0)),
#             salary_json_data.get("from", 0),
#             type(salary_json_data.get("from")),
#             salary_json_data.get("from"),
#         )
#         print(
#             type(salary_json_data.get("to", 0)),
#             salary_json_data.get("to", 0),
#             type(salary_json_data.get("to")),
#             salary_json_data.get("to"),
#         )
#         average_salary = (salary_json_data.get("from", 0) + salary_json_data.get("to", 0)) // 2
#         data.append(
#             {
#                 "id": row.get("id"),
#                 "name": row.get("name"),
#                 "area": area_json_data.get("name") or "Не указана",
#                 "salary": average_salary
#                 if salary_json_data.get("currency") == "RUR"
#                 else average_salary * 80,
#                 "experience": experience,
#                 "description": row.get("description", ""),
#                 "key_skills": key_skills,
#                 "alternate_url": row.get("alternate_url", ""),
#             }
#         )
#         print("end")

with open("vacancies.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        salary = int(row.get("salary") or 0)
        key_skills = row.get("key_skills", "").strip().split(",")
        key_skills = list(filter(None, key_skills))
        experience = 0
        match row.get("experience"):
            case "Нет опыта":
                experience = 0
            case "От 1 года до 3 лет":
                experience = 2
            case "От 3 до 6 лет":
                experience = 4
            case "Более 6 лет":
                experience = 6
        row["description"] = len(key_skills)
        row["experience"] = experience
        if all((salary, key_skills)):
            print(key_skills)
            data.append(row)


with open("vacancies2.csv", "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, data[0])
    dict_writer.writeheader()
    dict_writer.writerows(
        sorted(data, key=lambda i: (i["experience"], int(i["salary"]), len(i["key_skills"])), reverse=True)
    )

# with open("vacancies2.csv", "r", newline="", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     skills = []
#     for i, row in enumerate(reader):
#         skills += [sk.strip() for sk in row.get("key_skills", "").strip().split(",")]

# with open("skills.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(sorted(Counter(skills).items(), key=lambda i: -i[1]))  # type: ignore
