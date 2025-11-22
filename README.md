### Данный проект читает файл  с данными в формате csv и формирует отчет.
### Проект покрыт тестами на 99%.

### Технологии:
* Python
* tabulate
* Pytest

## Команда запуска скрипта:
python main.py --files employees1.csv employees2.csv --report performance

## Пример запуска скрипта:

## Отчет по эффективности работы разработчиков
| № | position | performance |
|---|----------|-------------|
| 1 | Backend Developer | 4.83 |
| 2 | DevOps Engineer | 4.80 |
| 3 | Data Engineer |  4.7 |
| 4 | Fullstack Developer | 4.7 |
| 5 | Frontend Developer  | 4.65 |
| 6 | Data Scientist  | 4.65 |
| 7 | Mobile Developer | 4.6 |
| 8 | QA Engineer | 4.5 |

## Чтобы добавить новый отчет, нужно:
1.	Создать новый класс в папке reports/
2.	Добавить его в список choices в main.py
3.	Добавить условие для его выполнения
