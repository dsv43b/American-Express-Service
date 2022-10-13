"""
Программа: Frontend часть проекта
Версия: 1.0
"""

import os

import yaml
import streamlit as st
from src.data.get_data import load_data, get_dataset
from src.plotting.charts import plot_data, distribution_number_records, target_value_distribution, old_new_customers
from src.train.training import start_training
from src.evaluate.evaluate import evaluate_input, evaluate_from_file

CONFIG_PATH = "../config/params.yml"


def main_page():
    """
    Страница с описанием проекта
    """
    st.image(
        "https://www.keeptheprice.com/img/loghi_pa/american_express.png",
        width=600,
    )

    st.markdown("# Описание проекта")
    st.title("American Express - Default Prediction 🏥")
    st.write(
        """
        Соревнование American Express - Default Prediction на сайте Kaggle.
        В соревновании предоставлены 3 файла с данными: тренировочные, 
        таргет значения для тренировочных данны и тестовые данные.\n
        Цель соревнования состоит в предсказании того, что клиент American Express 
        не вернет остаток средств по своей кредитной карте.\n 
        Если клиент не платил более 120 дней после последней выписки 
        ему присваивается целевое значение - 1, в ином случае целевое 
        значение равно 0.
        """
    )

    # Названия групп столбцов
    st.markdown(
        """
        ### Описание полей 
        В датасете присутствуют столбцы разделенные на следующие группы:\n
        D_: переменные просроченной задолженности;\n
        S_: расходные переменные;\n
        P_: платежные переменные;\n
        B_: балансовые переменные;\n
        R_*: переменные риска.
        """
    )


def exploratory():
    """
    Анализ данных
    """
    st.markdown("# Анализ данных")

    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # Загрузка и вывод датасета
    data = get_dataset(dataset_path=config["preprocessing"]["train_path"])
    st.write(data.head())
    st.markdown(
        '''
        Клиентам, которые не платят присваивается target значение - 1, 
        в ином случае target значение равно - 0.
        '''
    )

    # Построение графиков
    depending_on_date = st.sidebar.checkbox("Изменение кол-ва неплательщиков")
    number_records = st.sidebar.checkbox("Распределение по кол-ву записей")
    target_distribution = st.sidebar.checkbox("Распределение целевого значения")
    ratio_customers = st.sidebar.checkbox("Соотношение старых/новых клиентов")

    if depending_on_date:
        st.pyplot(
            plot_data(data=data)
        )
    if number_records:
        st.pyplot(
            distribution_number_records(data=data)
        )
    if target_distribution:
        st.pyplot(
            target_value_distribution(data=data)
        )
    if ratio_customers:
        st.pyplot(
            old_new_customers(data=data)
        )


def training():
    """
    Тренировка модели
    """
    st.markdown("# Тренировка модели CatBoost")
    # Получение параметров
    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    endpoint = config["endpoints"]["train"]

    if st.button("Start training"):
        start_training(config=config, endpoint=endpoint)


def prediction():
    """
    Получение предсказаний путем ввода данных
    """
    st.markdown("# Prediction")
    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    endpoint = config["endpoints"]["prediction_input"]
    unique_data_path = config["preprocessing"]["unique_values_path"]

    # проверка на наличие сохраненной модели
    if os.path.exists(config["train"]["model_path"]):
        evaluate_input(unique_data_path=unique_data_path, endpoint=endpoint)
    else:
        st.error("Сначала обучите модель")


def prediction_from_file():
    """
    Получение предсказаний из файла с данными
    """
    st.markdown("# Prediction")
    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    endpoint = config["endpoints"]["prediction_from_file"]

    upload_file = st.file_uploader(
        "", type=["ftr"], accept_multiple_files=False
    )
    # проверка загружен ли файл
    if upload_file:
        dataset_ftr_df, files = load_data(data=upload_file, type_data="Test")
        # проверка на наличие сохраненной модели
        if os.path.exists(config["train"]["model_path"]):
            evaluate_from_file(data=dataset_ftr_df, endpoint=endpoint, files=files)
        else:
            st.error("Сначала обучите модель")


def main():
    """
    Сборка пайплайна в одном блоке
    """
    page_names_to_funcs = {
        "Описание проекта": main_page,
        "Анализ данных": exploratory,
        "Тренировка модели": training,
        "Предсказание": prediction,
        "Предсказание из файла": prediction_from_file,
    }
    selected_page = st.sidebar.selectbox("Выберите пункт:", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()


if __name__ == "__main__":
    main()
