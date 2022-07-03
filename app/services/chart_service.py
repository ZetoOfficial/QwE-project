from collections import Counter

from app.cruds import CRUDChart
from app.cruds.vacancy import CRUDVacancy
from app.schemas import ExperienceSalary, PreviewInfo, SkillsDemand, SkillsSalary
from app.utils import average, median


class ChartService:
    @staticmethod
    async def get_skills_demand(limit: int) -> list[SkillsDemand]:
        skills = await CRUDChart.get_all_skills()
        only_skills = Counter(sum([skills["key_skills"] for skills in skills], [])).items()
        s_skills = sorted(only_skills, key=lambda x: x[1], reverse=True)[:limit]
        out = list()
        for skill in s_skills:
            out.append(SkillsDemand.parse_obj({"value": skill[1], "name": skill[0]}))
        return out

    @staticmethod
    async def get_skills_salary(limit: int) -> SkillsSalary:
        skills = await CRUDChart.get_all_skills()
        len_skills, salaries = [], []
        for key_skills, salary in skills:
            if len(key_skills) in len_skills:
                i = len_skills.index(len(key_skills))
                salaries[i] = average([salaries[i], salary], 1000)
                continue
            len_skills.append(len(key_skills))
            salaries.append(salary)
        x = zip(len_skills[:limit], salaries[:limit])
        xs = sorted(x, key=lambda i: i[1], reverse=True)
        return SkillsSalary.parse_obj({"len_skills": [x[0] for x in xs], "salary": [x[1] for x in xs]})

    @staticmethod
    async def get_experience_salary() -> ExperienceSalary:
        data = await CRUDChart.get_experience_and_salary()
        average_exp_salary_data = {}

        for exp, salary in sorted(data):
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

    @staticmethod
    async def get_preview_info() -> PreviewInfo:
        vacancies = await CRUDVacancy.get_all_vacancies()
        skills = await CRUDChart.get_all_skills()
        only_skills = sum([_["key_skills"] for _ in skills], [])
        return PreviewInfo.parse_obj(
            {
                "average_salary": median([vacancy.salary for vacancy in vacancies if vacancy.salary]),
                "average_exp": median([vacancy.experience for vacancy in vacancies]),
                "average_skills_names": " & ".join(
                    [skill[0] for skill in Counter(only_skills).most_common(3)]
                ),
                "average_skills_len": median(
                    [len(vacancy.key_skills) for vacancy in vacancies if vacancy.key_skills]
                ),
            }
        )
