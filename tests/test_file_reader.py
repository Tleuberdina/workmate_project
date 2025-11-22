import pytest

import os
import csv
import tempfile

from utils.file_reader import FileReader


class TestFileReader:
    """Тесты для класса FileReader."""
    def test_read_files_success(self, valid_csv_file):
        """Тест успешного чтения валидного CSV файла."""
        result = FileReader.read_files([valid_csv_file])
        assert len(result) == 3
        assert result[0]['name'] == 'John Smith'
        assert result[0]['position'] == 'Backend Developer'
        assert result[0]['completed_tasks'] == 42
        assert result[0]['performance'] == 4.8
        assert result[0]['experience_years'] == 5

    def test_read_files_multiple_files(self, multiple_csv_files):
        """Тест чтения нескольких CSV файлов."""
        result = FileReader.read_files(multiple_csv_files)
        assert len(result) == 4
        positions = [row['position'] for row in result]
        assert 'Backend Developer' in positions
        assert 'Frontend Developer' in positions
        assert 'Mobile Developer' in positions

    def test_read_files_missing_columns(self):
        """Тест чтения файла с отсутствующими колонками."""
        data = [
            ['name', 'position', 'completed_tasks'],
            ['John Smith', 'Backend Developer', '42']
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerows(data)
            temp_path = f.name
        with pytest.raises(ValueError, match='не содержит все необходимые колонки'):
            FileReader.read_files([temp_path])
        os.unlink(temp_path)

    def test_read_files_invalid_number_format(self):
        """Тест чтения файла с невалидными числовыми данными."""
        data = [
            ['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'],
            ['John Smith', 'Backend Developer', 'invalid', '4.8', 'Python', 'Backend Team', '5']
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerows(data)
            temp_path = f.name
        with pytest.raises(ValueError, match="invalid literal for int"):
            FileReader.read_files([temp_path])
        os.unlink(temp_path)

    def test_read_files_nonexistent_file(self):
        """Тест попытки чтения несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            FileReader.read_files(['nonexistent_file.csv'])

    def test_data_types_conversion(self, valid_csv_file):
        """Тест корректного преобразования типов данных."""
        result = FileReader.read_files([valid_csv_file])
        for row in result:
            assert isinstance(row['completed_tasks'], int)
            assert isinstance(row['performance'], float)
            assert isinstance(row['experience_years'], int)

    def test_empty_file(self):
        """Тест чтения пустого CSV файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
            temp_path = f.name
        result = FileReader.read_files([temp_path])
        assert result == []
        os.unlink(temp_path)
