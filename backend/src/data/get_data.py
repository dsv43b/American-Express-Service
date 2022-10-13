"""
Программа: Получение данных из файла
Версия: 1.0
"""

import pandas as pd


def get_dataset(dataset_path: str) -> pd.DataFrame:
    """
    Получение данных по заданному пути
    :param dataset_path: путь до данных
    :return: датасет
    """

    return pd.read_feather(dataset_path)
