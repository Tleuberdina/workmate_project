import csv
from typing import List, TypedDict


class EmployeeData(TypedDict):
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: str
    team: str
    experience_years: int


class FileReader:
    """Класс для чтения CSV файлов с данными о сотрудниках."""

    @staticmethod
    def read_files(file_paths: List[str]) -> List[EmployeeData]:
        """
        Читает данные из нескольких CSV файлов и объединяет их.
        """
        all_data: List[EmployeeData] = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    required_columns = ['name', 'position',
                                        'completed_tasks', 'performance',
                                        'skills', 'team', 'experience_years']
                    if not all(col in reader.fieldnames
                               for col in required_columns):
                        raise ValueError(f'Файл {file_path} '
                                         'не содержит все необходимые колонки')
                    for row in reader:
                        employee: EmployeeData = {
                            'name': row['name'],
                            'position': row['position'],
                            'completed_tasks': int(row['completed_tasks']),
                            'performance': float(row['performance']),
                            'skills': row['skills'],
                            'team': row['team'],
                            'experience_years': int(row['experience_years'])
                        }
                        all_data.append(employee)
            except Exception as e:
                print(f'Ошибка при чтении файла {file_path}: {e}')
                raise
        return all_data
