from .settings import BASE_DIR


class PepParsePipeline:
    """Суммирует количество документов PEP в разных статусах
    и по окончании парсинга формирует файл .csv."""

    def open_spider(self, spider):
        """Создает словарь для хранения статусов."""
        self.status_dict = {}

    def process_item(self, item, spider):
        """Считает кол-во PEP для каждого статуса."""
        status = item['status']
        if status not in self.status_dict.keys():
            self.status_dict[status] = 1
        else:
            self.status_dict[status] += 1
        return item

    def close_spider(self, spider):
        """Добавляет в .csv файл заголовок, данные о статусах
        и общее кол-во полученных PEP."""
        with open(
            f'{BASE_DIR}/results/status_summary_%(time)s.csv',
            mode='w',
            encoding='utf-8'
        ) as f:
            print('Статус,Количество', file=f)
            total = 0
            for status in self.status_dict:
                print(status, self.status_dict[status], file=f)
                total += int(self.status_dict[status])
            print(f'Total,{total}', file=f)
        self.session.close()
