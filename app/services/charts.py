from collections import Counter

from app.crud import get_all_skills, get_exp_and_salary, get_vacancies
from app.schemas import ExperienceSalary, PreviewInfo, SkillsDemand, SkillsSalary


def average(lst: list, base: int = 1) -> int:
    """Получение среднего числа с заданной точностью"""
    return round((sum(lst) / len(lst)) / base) * base


def get_skills_demand(limit: int) -> SkillsDemand:
    """Получение соотнесённых навыков с их частотой упоминания"""
    data = get_all_skills()
    only_skills = [skills["key_skills"] for skills in data]
    s_skills = sorted(Counter(only_skills).items(), key=lambda x: x[1], reverse=True)[:limit]
    return SkillsDemand.parse_obj([{"value": skill[1], "name": skill[0]} for skill in s_skills])


def get_skills_salary(limit: int) -> SkillsSalary:
    """Получение соотнесёности кол-ва навыков с заработной платой"""
    data = sorted(get_all_skills(), key=lambda k: k["salary"], reverse=True)[:limit]
    return SkillsSalary.parse_obj(
        {
            "len_skills": [len(skill["key_skills"]) for skill in data],
            "salary": [skill["salary"] for skill in data],
        }
    )


def preview_information() -> PreviewInfo:
    """Получение основной информации о навыках"""
    vacancies = get_vacancies()
    data = get_all_skills()
    only_skills = [skills["key_skills"] for skills in data]
    return PreviewInfo.parse_obj(
        {
            "average_salary": average([vacancy.salary for vacancy in vacancies], 1000),
            "average_exp": Counter([vacancy.experience for vacancy in vacancies]).most_common(1)[0][0],
            "average_skills_names": " & ".join([skill[0] for skill in Counter(only_skills).most_common(2)]),
            "average_skills_len": average(
                [len(vacancy.key_skills) for vacancy in vacancies if vacancy.key_skills]
            ),
        }
    )


def get_experience_salary() -> ExperienceSalary:
    """Получение соотнесёности навыков и средней зп"""
    data = get_exp_and_salary()
    average_exp_salary_data = {}
    for exp, salary in data:
        old_salary = average_exp_salary_data.get(exp, [])
        average_exp_salary_data[exp] = [*old_salary, salary]
    for exp, salaries in average_exp_salary_data.items():
        average_exp_salary_data[exp] = average(salaries, 1000)
    average_exp_salary_data = dict(sorted(average_exp_salary_data.items(), key=lambda item: item[1]))
    return ExperienceSalary.parse_obj(
        {
            "exp_names": [exp for exp, _ in average_exp_salary_data.items()],
            "avr_salary": [salary for _, salary in average_exp_salary_data.items()],
        }
    )
