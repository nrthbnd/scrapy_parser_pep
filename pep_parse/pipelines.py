import csv
import datetime
from collections import defaultdict

from .constants import BASE_DIR, RESULTS


class PepParsePipeline:
    """Суммирует количество документов PEP в разных статусах
    и по окончании парсинга формирует файл .csv."""

    def open_spider(self, spider):
        """Создает словарь для хранения статусов."""
        self.status_dict = defaultdict(int)

    def process_item(self, item, spider):
        """Считает кол-во PEP для каждого статуса."""
        status = item['status']
        self.status_dict[status] += 1
        return item

    def close_spider(self, spider):
        """Добавляет в .csv файл заголовок, данные о статусах
        и общее кол-во полученных PEP."""
        time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{time_str}.csv'
        with open(
            BASE_DIR / RESULTS / file_name,
            mode='w',
            encoding='utf-8',
        ) as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Статус', 'Количество'])
            status_data = [
                [status, count] for status, count in self.status_dict.items()]
            writer.writerows(status_data)
            total = sum(self.status_dict.values())
            writer.writerow(['Total', total])
        self.session.close()
