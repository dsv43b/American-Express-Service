"""
Программа: Предобработка числовых и категориальных данных
Версия: 1.0
"""

import pickle
import warnings

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import yaml
import json

warnings.filterwarnings("ignore")


def columns_omissions(data: pd.DataFrame, file_name: str, num_passes: float = 0.5) -> None:
    """
    Сохранение списка названия столбцов с большим количеством пропусков.
    Если относительное количеством пропусков превышает значение
    num_passes, то столбец попадает в список на удаление.

    :param data: датасет
    :param file_name: путь до файла для сохранения названия удаляемых столбцов
    :param num_passes: значение относительного кол-ва пропусков
    :return: None
    """

    many_passes_col = ['D_66']
    for i, j in zip(data.columns.to_list(), data.isnull().mean()):
        if j >= num_passes:
            many_passes_col.append(i)
    # Запись удаляемых столбцов в файл
    with open(file_name, 'w') as f:
        f.write(' '.join(many_passes_col))


def lable_coding(data: pd.DataFrame, categr_columns: list, path_name: str) -> None:
    """
    Обучение и сохранение кодировщиков для категориальных данных.

    :param data: датасет
    :param categr_columns: список названий категориальных столбцов
    :param path_name: путь до папки для сохранения кодировщиков
    :return: None
    """

    for categ in categr_columns:
        enc = LabelEncoder().fit(data[categ])
        with open(f'{path_name}/{categ}.pkl', 'wb') as f:
            pickle.dump(enc, f)


def lable_encoding(categ: str, path_name: str) -> LabelEncoder:
    """
    Возвращает обученный кодировщик для принятого названия категориального столбца.

    :param categ: название категориального столбца
    :param path_name: путь до папки с обученными кодировщиками
    :return: обученный кодировщик
    """

    with open(f'{path_name}/{categ}.pkl', 'rb') as f:
        enc = pickle.load(f)
    return enc


class PreprocessData:
    """
    Создание новых признаков для категориальных и числовых колонок. Для
    категориальных признаков: 'count', 'last', 'nunique'. Для числовых
    признаков: 'mean', 'std', 'min', 'max', 'last', 'quantile25', 'quantile50',
    'quantile75', '_diff'.
    """

    def __init__(self, categorical_col: list, numeric_col: list, encod_path_name: str):
        """
        :param categorical_col: список категориальных столбцов
        :param numeric_col: список числовых столбцов
        :param encod_path_name: путь до папки с обученными кодировщиками
        """
        self.categorical_col = categorical_col
        self.numeric_col = numeric_col
        self.encod_path_name = encod_path_name

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Объединение признаков.

        :param data: датасет
        :return: датасет с новыми признаками
        """

        result = pd.concat(
            [self.preproc_cat(data), self.preproc_num(data), self.diff_data(data)],
            axis=1)
        result.columns = [
            f'{i[0]}_{i[1]}' if len(i) == 2 else i for i in result.columns
        ]
        return result

    def preproc_cat(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Обработка категориальных данных.
        :param data: датасет
        :return: датасет с новыми признаками
        """

        # Применение трансформирования LabelEncoder к категориальным данным
        data[self.categorical_col] = data[self.categorical_col].apply(
            lambda col: lable_encoding(col.name, self.encod_path_name).transform(col))

        # Признаки для категориальных свойств
        data_cat = data.groupby("customer_ID")[self.categorical_col].agg(
            ['count', 'last', 'nunique']).astype('category')
        return data_cat

    def preproc_num(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Признаки для числовых свойств.
        :param data: датасет
        :return: датасет с новыми признаками
        """

        digt_group = data.groupby("customer_ID")[self.numeric_col]
        data_num_1 = digt_group.agg(['mean', 'std', 'min', 'max', 'last']) \
            .astype('float16')
        data_num_2 = digt_group.quantile([.25, .5, 0.75]).unstack() \
            .astype('float16')
        return pd.concat([data_num_1, data_num_2], axis=1)

    def diff_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Вычисление относительной разницы между последней и предпоследней
        датой для каждого признака.
        :param data: датасет
        :return: датасет с новыми признаками
        """
        digt_group = data.groupby("customer_ID")[self.numeric_col]
        data_num = digt_group.diff(1) / digt_group.shift(periods=1)
        data_num = data_num.add_suffix('_diff').astype('float16')
        data_num = pd.concat([data['customer_ID'], data_num], axis=1)
        data_num = data_num.groupby(['customer_ID']).last().astype('float16')
        return data_num


def feature_selection_corr(data: pd.DataFrame, path_name: str, corr_value: float = 0.9) -> None:
    """
    Сохранение названия столбцов в path_name со значением корреляции
    выше установленного в параметре corr_value.

    :param data: датасет
    :param path_name: путь до папки с обученными кодировщиками
    :param corr_value: значение корреляции выше которого признаки удаляются
    :return: None
    """

    deleted_colm = []
    left_colm = []

    corr_df = data.corr()
    for col in corr_df.columns:
        corr_list = corr_df[
            (corr_df[col].abs() > corr_value) & (corr_df[col].abs() != 1.0)
            ][col].index.to_list()
        if col not in deleted_colm:
            left_colm.append(col)
        deleted_colm.extend(corr_list)

    result = left_colm + data.select_dtypes('category').columns.to_list()
    with open(path_name, 'w') as f:
        f.write(' '.join(result))


def drop_columns(data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """
    Возвращает новый датасет с удаленными столбцами, названия
    которых сохраненны в file_name.

    :param data: датасет
    :param file_name: путь до файла
    :return: датасет с удаленными столбцами
    """

    with open(file_name, 'r') as f:
        drop_cols = f.read().split()
    return data.drop(columns=drop_cols)


def replacing_missing_values(data: pd.DataFrame,
                             change_to: float = -1000.) -> pd.DataFrame:
    """
    Замена пропущенных данных в числовых признаках.

    :param data: датасет
    :param change_to: значение, на которое заменяется пропущенные значения
    :return: датасет без пропущенными данными
    """

    float_data = data.select_dtypes('float16').columns.to_list()
    not_float = [i for i in data.columns.to_list() if i not in float_data]
    return pd.concat([
        data[not_float], data[float_data].fillna(change_to).astype('float16')
    ],
        axis=1)


def processing_target(data: pd.DataFrame, target_col: str) -> pd.Series:
    """
    Получение целевой переменной из датасета и присваивание каждому клиенту целевой переменной.

    :param data: датасет
    :param target_col: целевая переменная
    :return: датасет
    """

    return data.groupby('customer_ID')[target_col].last()


def pipeline_preprocess(data: pd.DataFrame, flg_evaluate: bool = True, **kwargs) -> pd.DataFrame:
    """
    Пайплайн по предобработке данных

    :param data: датасет
    :param flg_evaluate: флаг для evaluate
    :return: предобработанный датасет
    """

    data.sort_values(by=['customer_ID', 'S_2'], inplace=True)
    target_data = None
    if kwargs["target_column"] in data.columns:
        target_data = processing_target(data, kwargs["target_column"])
        data.drop(columns=kwargs["target_column"], inplace=True)

    # Получения столбцов с большим кол-ом пропусков
    if not flg_evaluate:
        columns_omissions(data, kwargs["drop_columns"])

    # Новый датафрейм с удаленными столбцали с большим кол-ом пропусков
    data = drop_columns(data, kwargs["drop_columns"])

    # Категориальные и цифровые колонки датасета
    cat_col = data.select_dtypes(include=['category']).columns.to_list()
    dig_col = [i for i in data.columns if i not in cat_col + ['S_2', 'customer_ID']]

    if not flg_evaluate:
        # Кодирование категориальных данных
        lable_coding(data, cat_col, kwargs["lable_encod_dir"])

    # Датасет с новыми признаками
    data = PreprocessData(cat_col, dig_col, kwargs["lable_encod_dir"])(data)

    if not flg_evaluate:
        # Сохранение списка столбцов с высокой корреляцией
        feature_selection_corr(data, kwargs["new_columns"])

    # Новый датафрейм с отобранными столбцами
    with open(kwargs["new_columns"], 'r') as f:
        new_colum = f.read().split()
    data = data[new_colum]

    # Замена пропущеных числовых значений
    data = replacing_missing_values(data)

    if target_data is not None:
        # Соединение датасета с целевым значением
        data = pd.concat([data, target_data], axis=1)

    return data


def make_dataframe(colum: list, features: list, config_path: str) -> pd.DataFrame:
    """
    Возвращает датасет полученный из переданных признаков, в датасете установлены категориальные и
    числовые колонки.

    :param colum: название колонок датасета
    :param features: признаки для датасета
    :param config_path: путь к конфигурационному файлу
    :return: предобработанный датасет
    """

    data = pd.DataFrame(data={col: feat for col, feat in zip(colum, features)}, index=[0])

    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    cat_col = config["preprocessing"]['categorical_input_data']
    dig_col = [i for i in data.columns if i not in cat_col + ['S_2', 'customer_ID']]

    data[cat_col] = data[cat_col].astype('category')
    data[dig_col] = data[dig_col].astype('float16')

    return data


def unique_features(data: pd.DataFrame, config_path: str) -> None:
    """
    Получение уникальных данных для категориальных столбцов, и максимольное и
    минимальное значение по числовым столбцам. Полученные данные сохраняются
    в json файле.

    :param data: датасет
    :param config_path: путь к конфигурационному файлу
    :return: None
    """

    result_cat = {i: data[i].unique().to_list() for i in
                  data.select_dtypes('category')}
    result_num = data.select_dtypes('float16').agg(['min', 'max']) \
        .to_dict('list')

    unique_data = {'categorical': result_cat, 'numeric': result_num}

    with open(config_path['unique_values_path'], 'w') as file:
        json.dump(unique_data, file)
