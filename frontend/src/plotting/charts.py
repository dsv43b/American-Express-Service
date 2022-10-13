"""
Программа: Отрисовка графиков
Версия: 1.0
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def plot_data(data: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    График изменения процента неплательщиков по времени.
    :param data: датасет
    :return: поле рисунка
    """

    fig = plt.figure(figsize=(15, 7))

    date_ser = data.groupby(['S_2'])['target'].mean()
    date_ser = date_ser.rolling('30D', min_periods=30).mean().mul(100)

    sns.lineplot(data=date_ser)
    plt.grid()
    plt.title("Изменение кол-ва неплательщиков", fontsize=20)
    plt.ylabel("Процент неплательщиков, %", fontsize=14)
    plt.xlabel('Дата', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    return fig


def barplot_group(df: pd.DataFrame, col_main: str, col_group: str, title: str) -> matplotlib.figure.Figure:
    """
    Построение гистограммы распределения

    :param df: датасет
    :param col_main: главный столбец
    :param col_group: столбец группировки
    :param title: тайтл графика
    :return: поле рисунка

    """

    fig = plt.figure(figsize=(17, 7))

    data = (df.groupby([col_group])[col_main]
            .value_counts(normalize=True)
            .rename('percentage')
            .mul(100)
            .reset_index()
            .sort_values(col_group))

    ax = sns.barplot(x=col_main, y="percentage", hue=col_group, data=data)

    for p in ax.patches:
        percentage = '{:.1f}%'.format(p.get_height())
        ax.annotate(percentage,
                    (p.get_x() + p.get_width() / 2.,
                     p.get_height()),
                    ha='center',
                    va='center',
                    xytext=(0, 10),
                    textcoords='offset points',
                    fontsize=10)

    plt.title(title, fontsize=20)
    plt.ylabel('Процент, %', fontsize=14)
    plt.xlabel(col_main, fontsize=14)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    return fig


def distribution_number_records(data: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    График распределения клиентов по количеству записей.

    :param data: датасет
    :return: поле рисунка
    """

    target_count = data.groupby(['customer_ID', 'target'])['S_2'].count()
    target_count = pd.DataFrame(target_count).reset_index() \
        .rename(columns={"S_2": "Counts"})

    return barplot_group(target_count, "Counts", "target", 'Распределение по кол-ву записей')


def target_value_distribution(data: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    Отрисовка графика barplot для распределения целевого значения.
    :param data: датасет
    :return: поле рисунка
    """

    fig = plt.figure(figsize=(10, 8))
    target_dist = data.groupby('customer_ID')['target'].last().value_counts(normalize=True).mul(100)

    ax = sns.barplot(
        x=target_dist.index,
        y=target_dist
    )

    for p in ax.patches:
        percentage = '{:.1f}%'.format(p.get_height())
        ax.annotate(percentage,
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center',
                    va='center',
                    xytext=(0, 10),
                    textcoords='offset points',
                    fontsize=14)
    plt.title("Распределение целевого значения")
    plt.ylabel("Процент распределения, %")
    plt.xlabel("Целевое значение")
    return fig


def old_new_customers(data: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    Отрисовка графика pie для определения соотношения между старыми и новыми
    клиентами. Старые клиенты - те которые имеют 13 записей, новые клиенты -
    те кто имеет меньше 13 записей.
    :param data: датасет
    :return: поле рисунка
    """

    data = data.groupby('customer_ID')['S_2'].count()

    fig = plt.figure(figsize=(8, 8))
    vals = [data[data < 13].shape[0], data[data == 13].shape[0]]
    labels = ['Новые клиенты', 'Старые клиенты']

    plt.pie(vals, labels=labels, explode=(0, 0.15), autopct='%1.1f%%')
    plt.title('Соотношение старых и новых клиентов')
    return fig
