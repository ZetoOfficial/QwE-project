from collections import Counter

from app.crud import get_all_skills, get_exp_and_salary, get_vacancies
from app.schemas import ExperienceSalary, PreviewInfo, SkillsDemand, SkillsSalary


def average(lst: list, base: int = 1) -> int:
    """Получение среднего числа с заданной точностью"""
    return round((sum(lst) / len(lst)) / base) * base


def median(lst: list):
    n = len(lst)
    index = n // 2
    if n % 2:
        return sorted(lst)[index]
    return sorted(lst)[index - 1 : index + 1][0]


def get_skills_demand(limit: int) -> list[SkillsDemand]:
    """Получение соотнесённых навыков с их частотой упоминания"""
    data = get_all_skills()
    only_skills = Counter(sum([skills["key_skills"] for skills in data], [])).items()
    s_skills = sorted(only_skills, key=lambda x: x[1], reverse=True)[:limit]
    return [
        SkillsDemand.parse_obj({"value": skill[1], "name": skill[0]})
        for skill in s_skills
    ]


def get_skills_salary(limit: int) -> SkillsSalary:
    """Получение соотнесённости кол-ва навыков с заработной платой"""
    data = sorted(get_all_skills(), key=lambda k: k["salary"], reverse=True)
    len_skills, salaries = [], []
    for skills, salary in data:
        if len(skills) in len_skills:
            i = len_skills.index(len(skills))
            salaries[i] = average([salaries[i], salary], 1000)
            continue
        len_skills.append(len(skills))
        salaries.append(salary)
    x = zip(len_skills[:limit], salaries[:limit])
    xs = sorted(x, key=lambda i: i[1], reverse=True)
    return SkillsSalary.parse_obj(
        {"len_skills": [x[0] for x in xs], "salary": [x[1] for x in xs]}
    )


def preview_information() -> PreviewInfo:
    """Получение основной информации о навыках"""
    vacancies = get_vacancies()
    data = get_all_skills()
    only_skills = sum([skills["key_skills"] for skills in data], [])
    return PreviewInfo.parse_obj(
        {
            "average_salary": median(
                [vacancy.salary for vacancy in vacancies if vacancy.salary]
            ),
            "average_exp": median([vacancy.experience for vacancy in vacancies]),
            "average_skills_names": " & ".join(
                [skill[0] for skill in Counter(only_skills).most_common(3)]
            ),
            "average_skills_len": median(
                [len(vacancy.key_skills) for vacancy in vacancies if vacancy.key_skills]
            ),
        }
    )


def get_experience_salary() -> ExperienceSalary:
    """Получение соотнесённости навыков и средней зп"""
    data = get_exp_and_salary()
    average_exp_salary_data = {}

    for exp, salary in sorted(data):
        old_salary = average_exp_salary_data.get(exp, [])
        average_exp_salary_data[exp] = [*old_salary, salary]

    for exp, salaries in average_exp_salary_data.items():
        average_exp_salary_data[exp] = average(salaries, 1000)
    average_exp_salary_data = dict(
        sorted(average_exp_salary_data.items(), key=lambda item: item[1])
    )
    return ExperienceSalary.parse_obj(
        {
            "exp_names": [exp for exp, _ in average_exp_salary_data.items()],
            "avr_salary": [salary for _, salary in average_exp_salary_data.items()],
        }
    )
