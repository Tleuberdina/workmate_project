from typing import List, Dict

from tabulate import tabulate

from utils.file_reader import EmployeeData, FileReader


class PerformanceReport:
    """Класс для генерации отчета по эффективности разработчиков."""

    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.data = None
        self.report_data = None

    def generate(self) -> None:
        """Генерирует отчет по эффективности."""
        self.data: List[EmployeeData] = FileReader.read_files(self.file_paths)
        position_performance = {}
        for employee in self.data:
            position = employee['position']
            performance = employee['performance']
            if position not in position_performance:
                position_performance[position] = {
                    'performances': [],
                    'count': 0
                }
            position_performance[position]['performances'].append(performance)
            position_performance[position]['count'] += 1
        self.report_data = []
        for position, stats in position_performance.items():
            avg_performance = sum(
                stats['performances']) / len(stats['performances']
                                             )
            self.report_data.append({
                'position': position,
                'avg_performance': avg_performance,
                'employee_count': stats['count']
            })
        self.report_data.sort(key=lambda x: x['avg_performance'], reverse=True)

    def display(self) -> None:
        """Отображает отчет в виде таблицы."""
        if not self.report_data:
            print('Нет данных для отображения')
            return
        table_data = []
        for i, row in enumerate(self.report_data, 1):
            table_data.append([
                i,
                row['position'],
                f'{row["avg_performance"]:.2f}'
            ])
        headers = ['№', 'position', 'performance']
        table = tabulate(table_data, headers=headers, tablefmt='fancy_grid')
        print('Отчет по эффективности работы разработчиков')
        print(table)

    def get_report_data(self) -> List[Dict]:
        """Возвращает данные отчета."""
        return self.report_data
