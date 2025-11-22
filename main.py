import argparse
import sys

from reports.performance_report import PerformanceReport


def main():
    parser = argparse.ArgumentParser(
        description='Анализ эффективности работы разработчиков'
        )
    parser.add_argument('--files', nargs='+', required=True,
                        help='Пути к CSV файлам с данными о сотрудниках')
    parser.add_argument('--report', required=True,
                        choices=['performance'],
                        help='Тип отчета для генерации')
    try:
        args = parser.parse_args()
    except SystemExit:
        print('Ошибка: неправильные аргументы.')
        sys.exit(1)
    for file_path in args.files:
        try:
            with open(file_path, 'r'):
                pass
        except FileNotFoundError:
            print(f'Ошибка: файл "{file_path}" не найден.')
            sys.exit(1)
        except IOError:
            print(f'Ошибка: невозможно прочитать файл "{file_path}".')
            sys.exit(1)
    if args.report == 'performance':
        report = PerformanceReport(args.files)
        report.generate()
        report.display()
    else:
        print(f'Ошибка: неизвестный тип отчета "{args.report}"')
        sys.exit(1)


if __name__ == '__main__':
    main()
