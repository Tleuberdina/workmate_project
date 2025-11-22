import pytest
from unittest.mock import patch

from main import main


class TestMain:
    """Тесты для главного модуля."""
    def test_main_success(self, capsys):
        """Тест успешного выполнения main."""
        test_args = ['main.py', '--files', 'test_data/valid_data.csv', 'test_data/missing_columns.csv', '--report', 'performance']
        with patch('sys.argv', test_args):
            with patch('main.PerformanceReport') as MockReport:
                mock_instance = MockReport.return_value
                main()
                MockReport.assert_called_once_with(['test_data/valid_data.csv', 'test_data/missing_columns.csv'])
                mock_instance.generate.assert_called_once()
                mock_instance.display.assert_called_once()

    def test_main_missing_arguments(self, capsys):
        """Тест вызова без обязательных аргументов."""
        test_args = ['main.py']
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            error_output = captured.out + captured.err
            assert 'неправильные аргументы' in error_output

    def test_main_file_not_found(self, capsys):
        """Тест с несуществующим файлом."""
        test_args = ['main.py', '--files', 'nonexistent.csv', '--report', 'performance']
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert 'не найден' in captured.out

    def test_main_unknown_report_type(self, capsys):
        """Тест с неизвестным типом отчета."""
        test_args = ['main.py', '--files', 'test_data/valid_data.csv', '--report', 'unknown']
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert 'неправильные аргументы' in captured.out

    def test_main_file_read_error(self, capsys):
        """Тест с ошибкой чтения файла."""
        test_args = ['main.py', '--files', 'test_data/valid_data.csv', '--report', 'performance']
        with patch('sys.argv', test_args):
            with patch('sys.exit') as mock_exit:
                with patch('builtins.open', side_effect=IOError("Read error")):
                    with patch('reports.performance_report.FileReader.read_files'):
                        main()
                        mock_exit.assert_called_once_with(1)
                        captured = capsys.readouterr()
                        assert 'невозможно прочитать файл' in captured.out
