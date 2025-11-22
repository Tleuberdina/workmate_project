import pytest
from unittest.mock import patch

from reports.performance_report import PerformanceReport


class TestPerformanceReport:
    """Тесты для класса PerformanceReport."""
    def test_generate_calculates_average_performance(self, performance_report_data):
        """Тест расчета средней эффективности."""
        report = PerformanceReport(['dummy_path.csv'])
        with patch('reports.performance_report.FileReader.read_files') as mock_read:
            mock_read.return_value = performance_report_data
            report.generate()
            assert len(report.report_data) == 2
            backend_data = next(item for item in report.report_data if item['position'] == 'Backend Developer')
            assert backend_data['avg_performance'] == pytest.approx(4.85)
            assert backend_data['employee_count'] == 2
            frontend_data = next(item for item in report.report_data if item['position'] == 'Frontend Developer')
            assert frontend_data['avg_performance'] == pytest.approx(4.3)
            assert frontend_data['employee_count'] == 1

    def test_generate_sorts_by_performance_descending(self, performance_report_data):
        """Тест сортировки по убыванию эффективности."""
        report = PerformanceReport(['dummy_path.csv'])
        with patch('reports.performance_report.FileReader.read_files') as mock_read:
            mock_read.return_value = performance_report_data
            report.generate()
            positions = [item['position'] for item in report.report_data]
            performances = [item['avg_performance'] for item in report.report_data]
            assert positions == ['Backend Developer', 'Frontend Developer']
            assert performances == [4.85, 4.3]
            assert performances[0] > performances[1]

    def test_generate_single_position_multiple_employees(self):
        """Тест расчета для одной должности с несколькими сотрудниками."""
        test_data = [
            {
                'name': 'Dev 1', 'position': 'Backend Developer', 'completed_tasks': 40,
                'performance': 4.5, 'skills': 'Python', 'team': 'Team A', 'experience_years': 3
            },
            {
                'name': 'Dev 2', 'position': 'Backend Developer', 'completed_tasks': 45,
                'performance': 4.7, 'skills': 'Java', 'team': 'Team A', 'experience_years': 4
            },
            {
                'name': 'Dev 3', 'position': 'Backend Developer', 'completed_tasks': 42,
                'performance': 4.6, 'skills': 'Go', 'team': 'Team B', 'experience_years': 2
            }
        ]
        report = PerformanceReport(['dummy_path.csv'])
        with patch('reports.performance_report.FileReader.read_files') as mock_read:
            mock_read.return_value = test_data
            report.generate()
            assert len(report.report_data) == 1
            assert report.report_data[0]['position'] == 'Backend Developer'
            assert report.report_data[0]['avg_performance'] == pytest.approx(4.6)
            assert report.report_data[0]['employee_count'] == 3

    def test_display_without_data(self, capsys):
        """Тест отображения когда нет данных."""
        report = PerformanceReport(['dummy_path.csv'])
        report.report_data = None
        report.display()
        captured = capsys.readouterr()
        assert 'Нет данных для отображения' in captured.out

    def test_display_with_data(self, capsys, performance_report_data):
        """Тест отображения отчета с данными."""
        report = PerformanceReport(['dummy_path.csv'])
        with patch('reports.performance_report.FileReader.read_files') as mock_read:
            mock_read.return_value = performance_report_data
            report.generate()
            report.display()
            captured = capsys.readouterr()
            assert 'Отчет по эффективности работы разработчиков' in captured.out
            assert "Backend Developer" in captured.out
            assert "Frontend Developer" in captured.out
            assert "4.85" in captured.out
            assert "4.3" in captured.out

    def test_get_report_data(self, performance_report_data):
        """Тест получения данных отчета."""
        report = PerformanceReport(['dummy_path.csv'])
        with patch('reports.performance_report.FileReader.read_files') as mock_read:
            mock_read.return_value = performance_report_data
            report.generate()
            result = report.get_report_data()
            assert result == report.report_data
            assert len(result) == 2

    def test_initial_state(self):
        """Тест начального состояния объекта."""
        report = PerformanceReport(['file1.csv', 'file2.csv'])
        assert report.file_paths == ['file1.csv', 'file2.csv']
        assert report.data is None
        assert report.report_data is None
