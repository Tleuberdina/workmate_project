import pytest

import os
import tempfile
import csv


@pytest.fixture
def valid_csv_file():
    """Создает временный CSV файл с валидными данными."""
    data = [
        ['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'],
        ['John Smith', 'Backend Developer', '42', '4.8', 'Python', 'Backend Team', '5'],
        ['Sarah Johnson', 'Frontend Developer', '38', '4.3', 'JavaScript', 'Frontend Team', '2'],
        ['Mike Brown', 'Backend Developer', '45', '4.9', 'Java', 'Backend Team', '4']
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerows(data)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def multiple_csv_files():
    """Создает несколько временных CSV файлов."""
    data1 = [
        ['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'],
        ['Dev 1', 'Backend Developer', '40', '4.5', 'Python', 'Team A', '3'],
        ['Dev 2', 'Frontend Developer', '35', '4.2', 'JavaScript', 'Team A', '2']
    ]
    data2 = [
        ['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'],
        ['Dev 3', 'Backend Developer', '45', '4.9', 'Java', 'Team B', '5'],
        ['Dev 4', 'Mobile Developer', '38', '4.4', 'Swift', 'Team B', '3']
    ]
    files = []
    for i, data in enumerate([data1, data2]):
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerows(data)
            files.append(f.name)
    yield files
    for file_path in files:
        os.unlink(file_path)


@pytest.fixture
def performance_report_data():
    """Возвращает тестовые данные для PerformanceReport."""
    return [
        {
            'name': 'John Smith',
            'position': 'Backend Developer',
            'completed_tasks': 42,
            'performance': 4.8,
            'skills': 'Python',
            'team': 'Backend Team',
            'experience_years': 5
        },
        {
            'name': 'Mike Brown',
            'position': 'Backend Developer',
            'completed_tasks': 45,
            'performance': 4.9,
            'skills': 'Java',
            'team': 'Backend Team',
            'experience_years': 4
        },
        {
            'name': 'Sarah Johnson',
            'position': 'Frontend Developer',
            'completed_tasks': 38,
            'performance': 4.3,
            'skills': 'JavaScript',
            'team': 'Frontend Team',
            'experience_years': 2
        }
    ]
