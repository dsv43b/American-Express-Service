"""
Программа: Отрисовка слайдеров и кнопок для ввода данных
с дальнейшим получением предсказания на основании введенных значений
Версия: 1.0
"""

import json
from io import BytesIO
import pandas as pd
import requests
import streamlit as st


def evaluate_input(unique_data_path: str, endpoint: object) -> None:
    """
    Получение входных данных путем ввода в UI -> вывод результата
    :param unique_data_path: путь до уникальных значений
    :param endpoint: endpoint
    """

    with open(unique_data_path) as file:
        unique_df = json.load(file)
    unique_df_cat = unique_df['categorical']
    unique_df_cat = remove_nan(unique_df_cat)
    unique_df_num = unique_df['numeric']

    # поля для вводы данных, категориальные данные
    customer_ID = st.text_input('customer_ID', '09d6bd597052cdcda90ffab')
    S_2 = st.text_input('S_2', '2017-04-07')

    D_63 = st.sidebar.selectbox("D_63", (unique_df_cat["D_63"]))
    D_64 = st.sidebar.selectbox("D_64", (unique_df_cat["D_64"]))
    D_66 = st.sidebar.selectbox("D_66", (unique_df_cat["D_66"]))
    D_68 = st.sidebar.selectbox("D_68", (unique_df_cat["D_68"]))
    B_30 = st.sidebar.selectbox("B_30", (unique_df_cat["B_30"]))
    B_38 = st.sidebar.selectbox("B_38", (unique_df_cat["B_38"]))
    D_114 = st.sidebar.selectbox("D_114", (unique_df_cat["D_114"]))
    D_116 = st.sidebar.selectbox("D_116", (unique_df_cat["D_116"]))
    D_117 = st.sidebar.selectbox("D_117", (unique_df_cat["D_117"]))
    D_120 = st.sidebar.selectbox("D_120", (unique_df_cat["D_120"]))
    D_126 = st.sidebar.selectbox("D_126", (unique_df_cat["D_126"]))

    # поля для вводы данных, числовые данные
    P_2 = st.sidebar.number_input("P_2", min_value=unique_df_num["P_2"][0], max_value=unique_df_num["P_2"][1])
    D_39 = st.sidebar.number_input("D_39", min_value=unique_df_num["D_39"][0], max_value=unique_df_num["D_39"][1])
    B_1 = st.sidebar.number_input("B_1", min_value=unique_df_num["B_1"][0], max_value=unique_df_num["B_1"][1])
    B_2 = st.sidebar.number_input("B_2", min_value=unique_df_num["B_2"][0], max_value=unique_df_num["B_2"][1])
    R_1 = st.sidebar.number_input("R_1", min_value=unique_df_num["R_1"][0], max_value=unique_df_num["R_1"][1])
    S_3 = st.sidebar.number_input("S_3", min_value=unique_df_num["S_3"][0], max_value=unique_df_num["S_3"][1])
    D_41 = st.sidebar.number_input("D_41", min_value=unique_df_num["D_41"][0], max_value=unique_df_num["D_41"][1])
    B_3 = st.sidebar.number_input("B_3", min_value=unique_df_num["B_3"][0], max_value=unique_df_num["B_3"][1])
    D_42 = st.sidebar.number_input("D_42", min_value=unique_df_num["D_42"][0], max_value=unique_df_num["D_42"][1])
    D_43 = st.sidebar.number_input("D_43", min_value=unique_df_num["D_43"][0], max_value=unique_df_num["D_43"][1])
    D_44 = st.sidebar.number_input("D_44", min_value=unique_df_num["D_44"][0], max_value=unique_df_num["D_44"][1])
    B_4 = st.sidebar.number_input("B_4", min_value=unique_df_num["B_4"][0], max_value=unique_df_num["B_4"][1])
    D_45 = st.sidebar.number_input("D_45", min_value=unique_df_num["D_45"][0], max_value=unique_df_num["D_45"][1])
    B_5 = st.sidebar.number_input("B_5", min_value=unique_df_num["B_5"][0], max_value=unique_df_num["B_5"][1])
    R_2 = st.sidebar.number_input("R_2", min_value=unique_df_num["R_2"][0], max_value=unique_df_num["R_2"][1])
    D_46 = st.sidebar.number_input("D_46", min_value=unique_df_num["D_46"][0], max_value=unique_df_num["D_46"][1])
    D_47 = st.sidebar.number_input("D_47", min_value=unique_df_num["D_47"][0], max_value=unique_df_num["D_47"][1])
    D_48 = st.sidebar.number_input("D_48", min_value=unique_df_num["D_48"][0], max_value=unique_df_num["D_48"][1])
    D_49 = st.sidebar.number_input("D_49", min_value=unique_df_num["D_49"][0], max_value=unique_df_num["D_49"][1])
    B_6 = st.sidebar.number_input("B_6", min_value=unique_df_num["B_6"][0], max_value=unique_df_num["B_6"][1])
    B_7 = st.sidebar.number_input("B_7", min_value=unique_df_num["B_7"][0], max_value=unique_df_num["B_7"][1])
    B_8 = st.sidebar.number_input("B_8", min_value=unique_df_num["B_8"][0], max_value=unique_df_num["B_8"][1])
    D_50 = st.sidebar.number_input("D_50", min_value=unique_df_num["D_50"][0], max_value=unique_df_num["D_50"][1])
    D_51 = st.sidebar.number_input("D_51", min_value=unique_df_num["D_51"][0], max_value=unique_df_num["D_51"][1])
    B_9 = st.sidebar.number_input("B_9", min_value=unique_df_num["B_9"][0], max_value=unique_df_num["B_9"][1])
    R_3 = st.sidebar.number_input("R_3", min_value=unique_df_num["R_3"][0], max_value=unique_df_num["R_3"][1])
    D_52 = st.sidebar.number_input("D_52", min_value=unique_df_num["D_52"][0], max_value=unique_df_num["D_52"][1])
    P_3 = st.sidebar.number_input("P_3", min_value=unique_df_num["P_3"][0], max_value=unique_df_num["P_3"][1])
    B_10 = st.sidebar.number_input("B_10", min_value=unique_df_num["B_10"][0], max_value=unique_df_num["B_10"][1])
    D_53 = st.sidebar.number_input("D_53", min_value=unique_df_num["D_53"][0], max_value=unique_df_num["D_53"][1])
    S_5 = st.sidebar.number_input("S_5", min_value=unique_df_num["S_5"][0], max_value=unique_df_num["S_5"][1])
    B_11 = st.sidebar.number_input("B_11", min_value=unique_df_num["B_11"][0], max_value=unique_df_num["B_11"][1])
    S_6 = st.sidebar.number_input("S_6", min_value=unique_df_num["S_6"][0], max_value=unique_df_num["S_6"][1])
    D_54 = st.sidebar.number_input("D_54", min_value=unique_df_num["D_54"][0], max_value=unique_df_num["D_54"][1])
    R_4 = st.sidebar.number_input("R_4", min_value=unique_df_num["R_4"][0], max_value=unique_df_num["R_4"][1])
    S_7 = st.sidebar.number_input("S_7", min_value=unique_df_num["S_7"][0], max_value=unique_df_num["S_7"][1])
    B_12 = st.sidebar.number_input("B_12", min_value=unique_df_num["B_12"][0], max_value=unique_df_num["B_12"][1])
    S_8 = st.sidebar.number_input("S_8", min_value=unique_df_num["S_8"][0], max_value=unique_df_num["S_8"][1])
    D_55 = st.sidebar.number_input("D_55", min_value=unique_df_num["D_55"][0], max_value=unique_df_num["D_55"][1])
    D_56 = st.sidebar.number_input("D_56", min_value=unique_df_num["D_56"][0], max_value=unique_df_num["D_56"][1])
    B_13 = st.sidebar.number_input("B_13", min_value=unique_df_num["B_13"][0], max_value=unique_df_num["B_13"][1])
    R_5 = st.sidebar.number_input("R_5", min_value=unique_df_num["R_5"][0], max_value=unique_df_num["R_5"][1])
    D_58 = st.sidebar.number_input("D_58", min_value=unique_df_num["D_58"][0], max_value=unique_df_num["D_58"][1])
    S_9 = st.sidebar.number_input("S_9", min_value=unique_df_num["S_9"][0], max_value=unique_df_num["S_9"][1])
    B_14 = st.sidebar.number_input("B_14", min_value=unique_df_num["B_14"][0], max_value=unique_df_num["B_14"][1])
    D_59 = st.sidebar.number_input("D_59", min_value=unique_df_num["D_59"][0], max_value=unique_df_num["D_59"][1])
    D_60 = st.sidebar.number_input("D_60", min_value=unique_df_num["D_60"][0], max_value=unique_df_num["D_60"][1])
    D_61 = st.sidebar.number_input("D_61", min_value=unique_df_num["D_61"][0], max_value=unique_df_num["D_61"][1])
    B_15 = st.sidebar.number_input("B_15", min_value=unique_df_num["B_15"][0], max_value=unique_df_num["B_15"][1])
    S_11 = st.sidebar.number_input("S_11", min_value=unique_df_num["S_11"][0], max_value=unique_df_num["S_11"][1])
    D_62 = st.sidebar.number_input("D_62", min_value=unique_df_num["D_62"][0], max_value=unique_df_num["D_62"][1])
    D_65 = st.sidebar.number_input("D_65", min_value=unique_df_num["D_65"][0], max_value=unique_df_num["D_65"][1])
    B_16 = st.sidebar.number_input("B_16", min_value=unique_df_num["B_16"][0], max_value=unique_df_num["B_16"][1])
    B_17 = st.sidebar.number_input("B_17", min_value=unique_df_num["B_17"][0], max_value=unique_df_num["B_17"][1])
    B_18 = st.sidebar.number_input("B_18", min_value=unique_df_num["B_18"][0], max_value=unique_df_num["B_18"][1])
    B_19 = st.sidebar.number_input("B_19", min_value=unique_df_num["B_19"][0], max_value=unique_df_num["B_19"][1])
    B_20 = st.sidebar.number_input("B_20", min_value=unique_df_num["B_20"][0], max_value=unique_df_num["B_20"][1])
    S_12 = st.sidebar.number_input("S_12", min_value=unique_df_num["S_12"][0], max_value=unique_df_num["S_12"][1])
    R_6 = st.sidebar.number_input("R_6", min_value=unique_df_num["R_6"][0], max_value=unique_df_num["R_6"][1])
    S_13 = st.sidebar.number_input("S_13", min_value=unique_df_num["S_13"][0], max_value=unique_df_num["S_13"][1])
    B_21 = st.sidebar.number_input("B_21", min_value=unique_df_num["B_21"][0], max_value=unique_df_num["B_21"][1])
    D_69 = st.sidebar.number_input("D_69", min_value=unique_df_num["D_69"][0], max_value=unique_df_num["D_69"][1])
    B_22 = st.sidebar.number_input("B_22", min_value=unique_df_num["B_22"][0], max_value=unique_df_num["B_22"][1])
    D_70 = st.sidebar.number_input("D_70", min_value=unique_df_num["D_70"][0], max_value=unique_df_num["D_70"][1])
    D_71 = st.sidebar.number_input("D_71", min_value=unique_df_num["D_71"][0], max_value=unique_df_num["D_71"][1])
    D_72 = st.sidebar.number_input("D_72", min_value=unique_df_num["D_72"][0], max_value=unique_df_num["D_72"][1])
    S_15 = st.sidebar.number_input("S_15", min_value=unique_df_num["S_15"][0], max_value=unique_df_num["S_15"][1])
    B_23 = st.sidebar.number_input("B_23", min_value=unique_df_num["B_23"][0], max_value=unique_df_num["B_23"][1])
    D_73 = st.sidebar.number_input("D_73", min_value=unique_df_num["D_73"][0], max_value=unique_df_num["D_73"][1])
    P_4 = st.sidebar.number_input("P_4", min_value=unique_df_num["P_4"][0], max_value=unique_df_num["P_4"][1])
    D_74 = st.sidebar.number_input("D_74", min_value=unique_df_num["D_74"][0], max_value=unique_df_num["D_74"][1])
    D_75 = st.sidebar.number_input("D_75", min_value=unique_df_num["D_75"][0], max_value=unique_df_num["D_75"][1])
    D_76 = st.sidebar.number_input("D_76", min_value=unique_df_num["D_76"][0], max_value=unique_df_num["D_76"][1])
    B_24 = st.sidebar.number_input("B_24", min_value=unique_df_num["B_24"][0], max_value=unique_df_num["B_24"][1])
    R_7 = st.sidebar.number_input("R_7", min_value=unique_df_num["R_7"][0], max_value=unique_df_num["R_7"][1])
    D_77 = st.sidebar.number_input("D_77", min_value=unique_df_num["D_77"][0], max_value=unique_df_num["D_77"][1])
    B_25 = st.sidebar.number_input("B_25", min_value=unique_df_num["B_25"][0], max_value=unique_df_num["B_25"][1])
    B_26 = st.sidebar.number_input("B_26", min_value=unique_df_num["B_26"][0], max_value=unique_df_num["B_26"][1])
    D_78 = st.sidebar.number_input("D_78", min_value=unique_df_num["D_78"][0], max_value=unique_df_num["D_78"][1])
    D_79 = st.sidebar.number_input("D_79", min_value=unique_df_num["D_79"][0], max_value=unique_df_num["D_79"][1])
    R_8 = st.sidebar.number_input("R_8", min_value=unique_df_num["R_8"][0], max_value=unique_df_num["R_8"][1])
    R_9 = st.sidebar.number_input("R_9", min_value=unique_df_num["R_9"][0], max_value=unique_df_num["R_9"][1])
    S_16 = st.sidebar.number_input("S_16", min_value=unique_df_num["S_16"][0], max_value=unique_df_num["S_16"][1])
    D_80 = st.sidebar.number_input("D_80", min_value=unique_df_num["D_80"][0], max_value=unique_df_num["D_80"][1])
    R_10 = st.sidebar.number_input("R_10", min_value=unique_df_num["R_10"][0], max_value=unique_df_num["R_10"][1])
    R_11 = st.sidebar.number_input("R_11", min_value=unique_df_num["R_11"][0], max_value=unique_df_num["R_11"][1])
    B_27 = st.sidebar.number_input("B_27", min_value=unique_df_num["B_27"][0], max_value=unique_df_num["B_27"][1])
    D_81 = st.sidebar.number_input("D_81", min_value=unique_df_num["D_81"][0], max_value=unique_df_num["D_81"][1])
    D_82 = st.sidebar.number_input("D_82", min_value=unique_df_num["D_82"][0], max_value=unique_df_num["D_82"][1])
    S_17 = st.sidebar.number_input("S_17", min_value=unique_df_num["S_17"][0], max_value=unique_df_num["S_17"][1])
    R_12 = st.sidebar.number_input("R_12", min_value=unique_df_num["R_12"][0], max_value=unique_df_num["R_12"][1])
    B_28 = st.sidebar.number_input("B_28", min_value=unique_df_num["B_28"][0], max_value=unique_df_num["B_28"][1])
    R_13 = st.sidebar.number_input("R_13", min_value=unique_df_num["R_13"][0], max_value=unique_df_num["R_13"][1])
    D_83 = st.sidebar.number_input("D_83", min_value=unique_df_num["D_83"][0], max_value=unique_df_num["D_83"][1])
    R_14 = st.sidebar.number_input("R_14", min_value=unique_df_num["R_14"][0], max_value=unique_df_num["R_14"][1])
    R_15 = st.sidebar.number_input("R_15", min_value=unique_df_num["R_15"][0], max_value=unique_df_num["R_15"][1])
    D_84 = st.sidebar.number_input("D_84", min_value=unique_df_num["D_84"][0], max_value=unique_df_num["D_84"][1])
    R_16 = st.sidebar.number_input("R_16", min_value=unique_df_num["R_16"][0], max_value=unique_df_num["R_16"][1])
    B_29 = st.sidebar.number_input("B_29", min_value=unique_df_num["B_29"][0], max_value=unique_df_num["B_29"][1])
    S_18 = st.sidebar.number_input("S_18", min_value=unique_df_num["S_18"][0], max_value=unique_df_num["S_18"][1])
    D_86 = st.sidebar.number_input("D_86", min_value=unique_df_num["D_86"][0], max_value=unique_df_num["D_86"][1])
    D_87 = st.sidebar.number_input("D_87", min_value=unique_df_num["D_87"][0], max_value=unique_df_num["D_87"][1])
    R_17 = st.sidebar.number_input("R_17", min_value=unique_df_num["R_17"][0], max_value=unique_df_num["R_17"][1])
    R_18 = st.sidebar.number_input("R_18", min_value=unique_df_num["R_18"][0], max_value=unique_df_num["R_18"][1])
    D_88 = st.sidebar.number_input("D_88", min_value=unique_df_num["D_88"][0], max_value=unique_df_num["D_88"][1])
    B_31 = st.sidebar.number_input("B_31", min_value=unique_df_num["B_31"][0], max_value=unique_df_num["B_31"][1])
    S_19 = st.sidebar.number_input("S_19", min_value=unique_df_num["S_19"][0], max_value=unique_df_num["S_19"][1])
    R_19 = st.sidebar.number_input("R_19", min_value=unique_df_num["R_19"][0], max_value=unique_df_num["R_19"][1])
    B_32 = st.sidebar.number_input("B_32", min_value=unique_df_num["B_32"][0], max_value=unique_df_num["B_32"][1])
    S_20 = st.sidebar.number_input("S_20", min_value=unique_df_num["S_20"][0], max_value=unique_df_num["S_20"][1])
    R_20 = st.sidebar.number_input("R_20", min_value=unique_df_num["R_20"][0], max_value=unique_df_num["R_20"][1])
    R_21 = st.sidebar.number_input("R_21", min_value=unique_df_num["R_21"][0], max_value=unique_df_num["R_21"][1])
    B_33 = st.sidebar.number_input("B_33", min_value=unique_df_num["B_33"][0], max_value=unique_df_num["B_33"][1])
    D_89 = st.sidebar.number_input("D_89", min_value=unique_df_num["D_89"][0], max_value=unique_df_num["D_89"][1])
    R_22 = st.sidebar.number_input("R_22", min_value=unique_df_num["R_22"][0], max_value=unique_df_num["R_22"][1])
    R_23 = st.sidebar.number_input("R_23", min_value=unique_df_num["R_23"][0], max_value=unique_df_num["R_23"][1])
    D_91 = st.sidebar.number_input("D_91", min_value=unique_df_num["D_91"][0], max_value=unique_df_num["D_91"][1])
    D_92 = st.sidebar.number_input("D_92", min_value=unique_df_num["D_92"][0], max_value=unique_df_num["D_92"][1])
    D_93 = st.sidebar.number_input("D_93", min_value=unique_df_num["D_93"][0], max_value=unique_df_num["D_93"][1])
    D_94 = st.sidebar.number_input("D_94", min_value=unique_df_num["D_94"][0], max_value=unique_df_num["D_94"][1])
    R_24 = st.sidebar.number_input("R_24", min_value=unique_df_num["R_24"][0], max_value=unique_df_num["R_24"][1])
    R_25 = st.sidebar.number_input("R_25", min_value=unique_df_num["R_25"][0], max_value=unique_df_num["R_25"][1])
    D_96 = st.sidebar.number_input("D_96", min_value=unique_df_num["D_96"][0], max_value=unique_df_num["D_96"][1])
    S_22 = st.sidebar.number_input("S_22", min_value=unique_df_num["S_22"][0], max_value=unique_df_num["S_22"][1])
    S_23 = st.sidebar.number_input("S_23", min_value=unique_df_num["S_23"][0], max_value=unique_df_num["S_23"][1])
    S_24 = st.sidebar.number_input("S_24", min_value=unique_df_num["S_24"][0], max_value=unique_df_num["S_24"][1])
    S_25 = st.sidebar.number_input("S_25", min_value=unique_df_num["S_25"][0], max_value=unique_df_num["S_25"][1])
    S_26 = st.sidebar.number_input("S_26", min_value=unique_df_num["S_26"][0], max_value=unique_df_num["S_26"][1])
    D_102 = st.sidebar.number_input("D_102", min_value=unique_df_num["D_102"][0], max_value=unique_df_num["D_102"][1])
    D_103 = st.sidebar.number_input("D_103", min_value=unique_df_num["D_103"][0], max_value=unique_df_num["D_103"][1])
    D_104 = st.sidebar.number_input("D_104", min_value=unique_df_num["D_104"][0], max_value=unique_df_num["D_104"][1])
    D_105 = st.sidebar.number_input("D_105", min_value=unique_df_num["D_105"][0], max_value=unique_df_num["D_105"][1])
    D_106 = st.sidebar.number_input("D_106", min_value=unique_df_num["D_106"][0], max_value=unique_df_num["D_106"][1])
    D_107 = st.sidebar.number_input("D_107", min_value=unique_df_num["D_107"][0], max_value=unique_df_num["D_107"][1])
    B_36 = st.sidebar.number_input("B_36", min_value=unique_df_num["B_36"][0], max_value=unique_df_num["B_36"][1])
    B_37 = st.sidebar.number_input("B_37", min_value=unique_df_num["B_37"][0], max_value=unique_df_num["B_37"][1])
    R_26 = st.sidebar.number_input("R_26", min_value=unique_df_num["R_26"][0], max_value=unique_df_num["R_26"][1])
    R_27 = st.sidebar.number_input("R_27", min_value=unique_df_num["R_27"][0], max_value=unique_df_num["R_27"][1])
    D_108 = st.sidebar.number_input("D_108", min_value=unique_df_num["D_108"][0], max_value=unique_df_num["D_108"][1])
    D_109 = st.sidebar.number_input("D_109", min_value=unique_df_num["D_109"][0], max_value=unique_df_num["D_109"][1])
    D_110 = st.sidebar.number_input("D_110", min_value=unique_df_num["D_110"][0], max_value=unique_df_num["D_110"][1])
    D_111 = st.sidebar.number_input("D_111", min_value=unique_df_num["D_111"][0], max_value=unique_df_num["D_111"][1])
    B_39 = st.sidebar.number_input("B_39", min_value=unique_df_num["B_39"][0], max_value=unique_df_num["B_39"][1])
    D_112 = st.sidebar.number_input("D_112", min_value=unique_df_num["D_112"][0], max_value=unique_df_num["D_112"][1])
    B_40 = st.sidebar.number_input("B_40", min_value=unique_df_num["B_40"][0], max_value=unique_df_num["B_40"][1])
    S_27 = st.sidebar.number_input("S_27", min_value=unique_df_num["S_27"][0], max_value=unique_df_num["S_27"][1])
    D_113 = st.sidebar.number_input("D_113", min_value=unique_df_num["D_113"][0], max_value=unique_df_num["D_113"][1])
    D_115 = st.sidebar.number_input("D_115", min_value=unique_df_num["D_115"][0], max_value=unique_df_num["D_115"][1])
    D_118 = st.sidebar.number_input("D_118", min_value=unique_df_num["D_118"][0], max_value=unique_df_num["D_118"][1])
    D_119 = st.sidebar.number_input("D_119", min_value=unique_df_num["D_119"][0], max_value=unique_df_num["D_119"][1])
    D_121 = st.sidebar.number_input("D_121", min_value=unique_df_num["D_121"][0], max_value=unique_df_num["D_121"][1])
    D_122 = st.sidebar.number_input("D_122", min_value=unique_df_num["D_122"][0], max_value=unique_df_num["D_122"][1])
    D_123 = st.sidebar.number_input("D_123", min_value=unique_df_num["D_123"][0], max_value=unique_df_num["D_123"][1])
    D_124 = st.sidebar.number_input("D_124", min_value=unique_df_num["D_124"][0], max_value=unique_df_num["D_124"][1])
    D_125 = st.sidebar.number_input("D_125", min_value=unique_df_num["D_125"][0], max_value=unique_df_num["D_125"][1])
    D_127 = st.sidebar.number_input("D_127", min_value=unique_df_num["D_127"][0], max_value=unique_df_num["D_127"][1])
    D_128 = st.sidebar.number_input("D_128", min_value=unique_df_num["D_128"][0], max_value=unique_df_num["D_128"][1])
    D_129 = st.sidebar.number_input("D_129", min_value=unique_df_num["D_129"][0], max_value=unique_df_num["D_129"][1])
    B_41 = st.sidebar.number_input("B_41", min_value=unique_df_num["B_41"][0], max_value=unique_df_num["B_41"][1])
    B_42 = st.sidebar.number_input("B_42", min_value=unique_df_num["B_42"][0], max_value=unique_df_num["B_42"][1])
    D_130 = st.sidebar.number_input("D_130", min_value=unique_df_num["D_130"][0], max_value=unique_df_num["D_130"][1])
    D_131 = st.sidebar.number_input("D_131", min_value=unique_df_num["D_131"][0], max_value=unique_df_num["D_131"][1])
    D_132 = st.sidebar.number_input("D_132", min_value=unique_df_num["D_132"][0], max_value=unique_df_num["D_132"][1])
    D_133 = st.sidebar.number_input("D_133", min_value=unique_df_num["D_133"][0], max_value=unique_df_num["D_133"][1])
    R_28 = st.sidebar.number_input("R_28", min_value=unique_df_num["R_28"][0], max_value=unique_df_num["R_28"][1])
    D_134 = st.sidebar.number_input("D_134", min_value=unique_df_num["D_134"][0], max_value=unique_df_num["D_134"][1])
    D_135 = st.sidebar.number_input("D_135", min_value=unique_df_num["D_135"][0], max_value=unique_df_num["D_135"][1])
    D_136 = st.sidebar.number_input("D_136", min_value=unique_df_num["D_136"][0], max_value=unique_df_num["D_136"][1])
    D_137 = st.sidebar.number_input("D_137", min_value=unique_df_num["D_137"][0], max_value=unique_df_num["D_137"][1])
    D_138 = st.sidebar.number_input("D_138", min_value=unique_df_num["D_138"][0], max_value=unique_df_num["D_138"][1])
    D_139 = st.sidebar.number_input("D_139", min_value=unique_df_num["D_139"][0], max_value=unique_df_num["D_139"][1])
    D_140 = st.sidebar.number_input("D_140", min_value=unique_df_num["D_140"][0], max_value=unique_df_num["D_140"][1])
    D_141 = st.sidebar.number_input("D_141", min_value=unique_df_num["D_141"][0], max_value=unique_df_num["D_141"][1])
    D_142 = st.sidebar.number_input("D_142", min_value=unique_df_num["D_142"][0], max_value=unique_df_num["D_142"][1])
    D_143 = st.sidebar.number_input("D_143", min_value=unique_df_num["D_143"][0], max_value=unique_df_num["D_143"][1])
    D_144 = st.sidebar.number_input("D_144", min_value=unique_df_num["D_144"][0], max_value=unique_df_num["D_144"][1])
    D_145 = st.sidebar.number_input("D_145", min_value=unique_df_num["D_145"][0], max_value=unique_df_num["D_145"][1])

    # gender = st.sidebar.selectbox("Gender", (unique_df["Gender"]))
    # age = st.sidebar.slider("Age", min_value=min(unique_df["Age"]), max_value=max(unique_df["Age"]))
    # driving_license = st.sidebar.selectbox("Driving_License", (unique_df["Driving_License"]))

    dict_data = {
        "customer_ID": customer_ID,
        "S_2": S_2,
        "P_2": P_2,
        "D_39": D_39,
        "B_1": B_1,
        "B_2": B_2,
        "R_1": R_1,
        "S_3": S_3,
        "D_41": D_41,
        "B_3": B_3,
        "D_42": D_42,
        "D_43": D_43,
        "D_44": D_44,
        "B_4": B_4,
        "D_45": D_45,
        "B_5": B_5,
        "R_2": R_2,
        "D_46": D_46,
        "D_47": D_47,
        "D_48": D_48,
        "D_49": D_49,
        "B_6": B_6,
        "B_7": B_7,
        "B_8": B_8,
        "D_50": D_50,
        "D_51": D_51,
        "B_9": B_9,
        "R_3": R_3,
        "D_52": D_52,
        "P_3": P_3,
        "B_10": B_10,
        "D_53": D_53,
        "S_5": S_5,
        "B_11": B_11,
        "S_6": S_6,
        "D_54": D_54,
        "R_4": R_4,
        "S_7": S_7,
        "B_12": B_12,
        "S_8": S_8,
        "D_55": D_55,
        "D_56": D_56,
        "B_13": B_13,
        "R_5": R_5,
        "D_58": D_58,
        "S_9": S_9,
        "B_14": B_14,
        "D_59": D_59,
        "D_60": D_60,
        "D_61": D_61,
        "B_15": B_15,
        "S_11": S_11,
        "D_62": D_62,
        "D_63": D_63,
        "D_64": D_64,
        "D_65": D_65,
        "B_16": B_16,
        "B_17": B_17,
        "B_18": B_18,
        "B_19": B_19,
        "D_66": D_66,
        "B_20": B_20,
        "D_68": D_68,
        "S_12": S_12,
        "R_6": R_6,
        "S_13": S_13,
        "B_21": B_21,
        "D_69": D_69,
        "B_22": B_22,
        "D_70": D_70,
        "D_71": D_71,
        "D_72": D_72,
        "S_15": S_15,
        "B_23": B_23,
        "D_73": D_73,
        "P_4": P_4,
        "D_74": D_74,
        "D_75": D_75,
        "D_76": D_76,
        "B_24": B_24,
        "R_7": R_7,
        "D_77": D_77,
        "B_25": B_25,
        "B_26": B_26,
        "D_78": D_78,
        "D_79": D_79,
        "R_8": R_8,
        "R_9": R_9,
        "S_16": S_16,
        "D_80": D_80,
        "R_10": R_10,
        "R_11": R_11,
        "B_27": B_27,
        "D_81": D_81,
        "D_82": D_82,
        "S_17": S_17,
        "R_12": R_12,
        "B_28": B_28,
        "R_13": R_13,
        "D_83": D_83,
        "R_14": R_14,
        "R_15": R_15,
        "D_84": D_84,
        "R_16": R_16,
        "B_29": B_29,
        "B_30": B_30,
        "S_18": S_18,
        "D_86": D_86,
        "D_87": D_87,
        "R_17": R_17,
        "R_18": R_18,
        "D_88": D_88,
        "B_31": B_31,
        "S_19": S_19,
        "R_19": R_19,
        "B_32": B_32,
        "S_20": S_20,
        "R_20": R_20,
        "R_21": R_21,
        "B_33": B_33,
        "D_89": D_89,
        "R_22": R_22,
        "R_23": R_23,
        "D_91": D_91,
        "D_92": D_92,
        "D_93": D_93,
        "D_94": D_94,
        "R_24": R_24,
        "R_25": R_25,
        "D_96": D_96,
        "S_22": S_22,
        "S_23": S_23,
        "S_24": S_24,
        "S_25": S_25,
        "S_26": S_26,
        "D_102": D_102,
        "D_103": D_103,
        "D_104": D_104,
        "D_105": D_105,
        "D_106": D_106,
        "D_107": D_107,
        "B_36": B_36,
        "B_37": B_37,
        "R_26": R_26,
        "R_27": R_27,
        "B_38": B_38,
        "D_108": D_108,
        "D_109": D_109,
        "D_110": D_110,
        "D_111": D_111,
        "B_39": B_39,
        "D_112": D_112,
        "B_40": B_40,
        "S_27": S_27,
        "D_113": D_113,
        "D_114": D_114,
        "D_115": D_115,
        "D_116": D_116,
        "D_117": D_117,
        "D_118": D_118,
        "D_119": D_119,
        "D_120": D_120,
        "D_121": D_121,
        "D_122": D_122,
        "D_123": D_123,
        "D_124": D_124,
        "D_125": D_125,
        "D_126": D_126,
        "D_127": D_127,
        "D_128": D_128,
        "D_129": D_129,
        "B_41": B_41,
        "B_42": B_42,
        "D_130": D_130,
        "D_131": D_131,
        "D_132": D_132,
        "D_133": D_133,
        "R_28": R_28,
        "D_134": D_134,
        "D_135": D_135,
        "D_136": D_136,
        "D_137": D_137,
        "D_138": D_138,
        "D_139": D_139,
        "D_140": D_140,
        "D_141": D_141,
        "D_142": D_142,
        "D_143": D_143,
        "D_144": D_144,
        "D_145": D_145
    }

    st.write(
        f"""### Данные клиента:\n
    customer_ID: {customer_ID},
    S_2: {S_2},
    D_63: {D_63},
    D_64: {D_64},
    D_66: {D_66},
    D_68: {D_68},
    B_30: {B_30},
    B_38: {B_38},
    D_114: {D_114},
    D_116: {D_116},
    D_117: {D_117},
    D_120: {D_120},
    D_126: {D_126},
    
    P_2: {P_2},
    D_39: {D_39},
    B_1: {B_1},
    B_2: {B_2},
    R_1: {R_1},
    S_3: {S_3},
    D_41: {D_41},
    B_3: {B_3},
    D_42: {D_42},
    D_43: {D_43},
    D_44: {D_44},
    B_4: {B_4},
    D_45: {D_45},
    B_5: {B_5},
    R_2: {R_2},
    D_46: {D_46},
    D_47: {D_47},
    D_48: {D_48},
    D_49: {D_49},
    B_6: {B_6},
    B_7: {B_7},
    B_8: {B_8},
    D_50: {D_50},
    D_51: {D_51},
    B_9: {B_9},
    R_3: {R_3},
    D_52: {D_52},
    P_3: {P_3},
    B_10: {B_10},
    D_53: {D_53},
    S_5: {S_5},
    B_11: {B_11},
    S_6: {S_6},
    D_54: {D_54},
    R_4: {R_4},
    S_7: {S_7},
    B_12: {B_12},
    S_8: {S_8},
    D_55: {D_55},
    D_56: {D_56},
    B_13: {B_13},
    R_5: {R_5},
    D_58: {D_58},
    S_9: {S_9},
    B_14: {B_14},
    D_59: {D_59},
    D_60: {D_60},
    D_61: {D_61},
    B_15: {B_15},
    S_11: {S_11},
    D_62: {D_62},
    D_65: {D_65},
    B_16: {B_16},
    B_17: {B_17},
    B_18: {B_18},
    B_19: {B_19},
    B_20: {B_20},
    S_12: {S_12},
    R_6: {R_6},
    S_13: {S_13},
    B_21: {B_21},
    D_69: {D_69},
    B_22: {B_22},
    D_70: {D_70},
    D_71: {D_71},
    D_72: {D_72},
    S_15: {S_15},
    B_23: {B_23},
    D_73: {D_73},
    P_4: {P_4},
    D_74: {D_74},
    D_75: {D_75},
    D_76: {D_76},
    B_24: {B_24},
    R_7: {R_7},
    D_77: {D_77},
    B_25: {B_25},
    B_26: {B_26},
    D_78: {D_78},
    D_79: {D_79},
    R_8: {R_8},
    R_9: {R_9},
    S_16: {S_16},
    D_80: {D_80},
    R_10: {R_10},
    R_11: {R_11},
    B_27: {B_27},
    D_81: {D_81},
    D_82: {D_82},
    S_17: {S_17},
    R_12: {R_12},
    B_28: {B_28},
    R_13: {R_13},
    D_83: {D_83},
    R_14: {R_14},
    R_15: {R_15},
    D_84: {D_84},
    R_16: {R_16},
    B_29: {B_29},
    S_18: {S_18},
    D_86: {D_86},
    D_87: {D_87},
    R_17: {R_17},
    R_18: {R_18},
    D_88: {D_88},
    B_31: {B_31},
    S_19: {S_19},
    R_19: {R_19},
    B_32: {B_32},
    S_20: {S_20},
    R_20: {R_20},
    R_21: {R_21},
    B_33: {B_33},
    D_89: {D_89},
    R_22: {R_22},
    R_23: {R_23},
    D_91: {D_91},
    D_92: {D_92},
    D_93: {D_93},
    D_94: {D_94},
    R_24: {R_24},
    R_25: {R_25},
    D_96: {D_96},
    S_22: {S_22},
    S_23: {S_23},
    S_24: {S_24},
    S_25: {S_25},
    S_26: {S_26},
    D_102: {D_102},
    D_103: {D_103},
    D_104: {D_104},
    D_105: {D_105},
    D_106: {D_106},
    D_107: {D_107},
    B_36: {B_36},
    B_37: {B_37},
    R_26: {R_26},
    R_27: {R_27},
    D_108: {D_108},
    D_109: {D_109},
    D_110: {D_110},
    D_111: {D_111},
    B_39: {B_39},
    D_112: {D_112},
    B_40: {B_40},
    S_27: {S_27},
    D_113: {D_113},
    D_115: {D_115},
    D_118: {D_118},
    D_119: {D_119},
    D_121: {D_121},
    D_122: {D_122},
    D_123: {D_123},
    D_124: {D_124},
    D_125: {D_125},
    D_127: {D_127},
    D_128: {D_128},
    D_129: {D_129},
    B_41: {B_41},
    B_42: {B_42},
    D_130: {D_130},
    D_131: {D_131},
    D_132: {D_132},
    D_133: {D_133},
    R_28: {R_28},
    D_134: {D_134},
    D_135: {D_135},
    D_136: {D_136},
    D_137: {D_137},
    D_138: {D_138},
    D_139: {D_139},
    D_140: {D_140},
    D_141: {D_141},
    D_142: {D_142},
    D_143: {D_143},
    D_144: {D_144},
    D_145: {D_145}
    """
    )

    # Предсказание целевого значения
    button_ok = st.button("Predict")
    if button_ok:
        result = requests.post(endpoint, timeout=8000, json=dict_data)
        json_str = json.dumps(result.json())
        output = json.loads(json_str)
        st.write(f"## {output}")
        st.success("Success!")


def remove_nan(input_dict):
    new_d = {}
    for k, v in input_dict.items():
        v_copy = list(map(str, v))
        if 'nan' in v_copy:
            numb = v_copy.index('nan')
            v.pop(numb)
        new_d[k] = v
    return new_d


def evaluate_from_file(data: pd.DataFrame, endpoint: object, files: BytesIO):
    """
    Получение входных данных в качестве файла -> вывод результата в виде таблицы
    :param data: датасет
    :param endpoint: endpoint
    :param files:
    """

    button_ok = st.button("Predict")
    if button_ok:
        # заглушка так как не выводим все предсказания
        unique_id = data['customer_ID'].unique()[:5]
        data_ = pd.DataFrame(unique_id, columns=['customer_ID'])
        output = requests.post(endpoint, files=files, timeout=8000)
        data_["predict"] = output.json()["prediction"]
        st.write(data_.head())
