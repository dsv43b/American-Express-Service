"""
Программа: Сборный конвейер для тренировки модели
Версия: 1.0
"""

import joblib
import yaml

from ..data.split_dataset import split_train_test
from ..train.train import find_optimal_params, train_model
from ..data.get_data import get_dataset
from ..transform.transform import pipeline_preprocess, unique_features
import logging


def pipeline_training(config_path: str) -> None:
    """
    Полный цикл получения данных, предобработки и тренировки модели
    :param config_path: путь до файла с конфигурациями
    :return: None
    """

    # Получение параметров
    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    preprocessing_config = config["preprocessing"]
    train_config = config["train"]

    # Получение тренировочных данных
    logging.info('Начата загрузка тренировочных данных...')
    train_data = get_dataset(dataset_path=preprocessing_config["train_path"])
    logging.info('Тренeровочных данные загружены!!!')

    # Получение уникальных данных по столбцами
    unique_features(train_data, preprocessing_config)
    logging.info('Создан файл с уникальными значениями столбцов!!!')

    # Предобработка данных
    logging.info('Начата обработка тренировочных данных...')
    train_data = pipeline_preprocess(data=train_data, flg_evaluate=False, **preprocessing_config)
    logging.info('Обработка тренировочных данных завершена!!!')

    # Разделение датасета на тренировочный и тестовый
    df_train, df_test = split_train_test(dataset=train_data, **preprocessing_config)
    logging.info('Данные разделены на тестовые и тренировочные!!!')

    # Поиск оптимальных параметров для модели
    logging.info('Начата поиск оптимальных параметров для модели...')
    cat_column = train_data.select_dtypes('category').columns.to_list()
    study = find_optimal_params(data_train=df_train, data_test=df_test, cat_features=cat_column, **train_config)
    logging.info('Поиск оптимальных параметров завершен!!!')

    # Тренировка модели с лучшими параметрами
    logging.info('Начата тренировка модели с оптимальными параметрами...')
    clf = train_model(
        data_train=df_train,
        data_test=df_test,
        study=study,
        cat_features=cat_column,
        target=preprocessing_config["target_column"],
        metric_path=train_config["metrics_path"],
    )
    logging.info('Тренировка модели завершена!!!')

    # Сохранение моделей (study, model)
    joblib.dump(clf, train_config["model_path"])
    joblib.dump(study, train_config["study_path"])
    logging.info('Модели сохранены!!!')
