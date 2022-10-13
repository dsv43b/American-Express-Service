"""
Программа: Модель для прогнозирования того, погасит клиент American Express,
свою задолженость перед компанией или нет.
Версия: 1.0
"""

import warnings
import optuna

import uvicorn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from src.pipelines.pipeline import pipeline_training
from src.evaluate.evaluate import pipeline_evaluate
from src.train.metrics import load_metrics
from src.transform.transform import make_dataframe
import logging
import yaml

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

app = FastAPI()
CONFIG_PATH = "../config/params.yml"

# Создание логирующего файла
with open(CONFIG_PATH) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
preprocessing_config = config["preprocessing"]

logging.basicConfig(handlers=[logging.FileHandler(filename=preprocessing_config['log_file'],
                                                  encoding='utf-8', mode='w')],
                    format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.INFO)


class InsuranceCustomer(BaseModel):
    """
    Признаки для получения результатов модели
    """

    customer_ID: str = '00000469ba478561f23a'
    S_2: str = '2019-04-10'
    P_2: float = 0.953125
    D_39: float = 0.00982666015625
    B_1: float = 0.00563812255859375
    B_2: float = 0.8134765625
    R_1: float = 0.0030498504638671875
    S_3: float = -1
    D_41: float = 0.0007500648498535156
    B_3: float = 0.00928497314453125
    D_42: float = 0.00891876220703125
    D_43: float = 0.0543212890625
    D_44: float = 0.0013780593872070312
    B_4: float = 0.30419921875
    D_45: float = 0.00865936279296875
    B_5: float = 9.995698928833008e-05
    R_2: float = 0.00390625
    D_46: float = 0.24169921875
    D_47: float = 0.65234375
    D_48: float = 0.053558349609375
    D_49: float = -1
    B_6: float = 0.2293701171875
    B_7: float = 0.060791015625
    B_8: float = 1.001953125
    D_50: float = 0.83154296875
    D_51: float = 0.6728515625
    B_9: float = 0.0018262863159179688
    R_3: float = 0.1005859375
    D_52: float = 0.5048828125
    P_3: float = 0.65234375
    B_10: float = 0.1536865234375
    D_53: float = -1
    S_5: float = 0.00021457672119140625
    B_11: float = 0.007183074951171875
    S_6: float = 1.0068359375
    D_54: float = 1.0087890625
    R_4: float = 0.003787994384765625
    S_7: float = -1
    B_12: float = 0.0095672607421875
    S_8: float = 0.007160186767578125
    D_55: float = 0.1453857421875
    D_56: float = 0.7099609375
    B_13: float = 0.007381439208984375
    R_5: float = 0.00820159912109375
    D_58: float = 0.12322998046875
    S_9: float = -1
    B_14: float = 0.007701873779296875
    D_59: float = 0.06561279296875
    D_60: float = 0.0022983551025390625
    D_61: float = 0.6630859375
    B_15: float = 0.0005383491516113281
    S_11: float = 0.409912109375
    D_62: float = 1.0849609375
    D_63: str = 'CO'
    D_64: str = 'O'
    D_65: float = 0.006435394287109375
    B_16: float = 0.00794219970703125
    B_17: float = -1
    B_18: float = 0.478271484375
    B_19: float = 0.004150390625
    D_66: float = 0
    B_20: float = 0.0028972625732421875
    D_68: float = 6.0
    S_12: float = 0.18505859375
    R_6: float = 0.00489044189453125
    S_13: float = 0.004871368408203125
    B_21: float = 0.0027484893798828125
    D_69: float = 0.00901031494140625
    B_22: float = 0.003971099853515625
    D_70: float = 0.0038700103759765625
    D_71: float = 0.312255859375
    D_72: float = 0.0078125
    S_15: float = 0.50244140625
    B_23: float = 0.049346923828125
    D_73: float = -1
    P_4: float = 0.96533203125
    D_74: float = 0.078857421875
    D_75: float = 0.069091796875
    D_76: float = -1
    B_24: float = 0.007495880126953125
    R_7: float = 0.0035400390625
    D_77: float = 1.005859375
    B_25: float = 0.009979248046875
    B_26: float = 0.00493621826171875
    D_78: float = 0.00910186767578125
    D_79: float = 0.005001068115234375
    R_8: float = 0.0033130645751953125
    R_9: float = -1
    S_16: float = 0.007049560546875
    D_80: float = 0.208984375
    R_10: float = 0.0023975372314453125
    R_11: float = 0.00620269775390625
    B_27: float = 0.0030345916748046875
    D_81: float = 0.006282806396484375
    D_82: float = -1
    S_17: float = 0.00734710693359375
    R_12: float = 1.0009765625
    B_28: float = 0.33203125
    R_13: float = 0.0099945068359375
    D_83: float = 0.00038433074951171875
    R_14: float = 0.00853729248046875
    R_15: float = 0.0062255859375
    D_84: float = 0.0003535747528076172
    R_16: float = 0.005367279052734375
    B_29: float = -1
    B_30: float = 0.0
    S_18: float = 0.001918792724609375
    D_86: float = 0.00937652587890625
    D_87: float = -1
    R_17: float = 0.009429931640625
    R_18: float = 0.0012989044189453125
    D_88: float = -1
    B_31: float = 1.0
    S_19: float = 0.009002685546875
    R_19: float = 0.00241851806640625
    B_32: float = 0.005084991455078125
    S_20: float = 0.00682830810546875
    R_20: float = 0.0002567768096923828
    R_21: float = 0.005702972412109375
    B_33: float = 1.0087890625
    D_89: float = 0.0006775856018066406
    R_22: float = 0.00899505615234375
    R_23: float = 0.00984954833984375
    D_91: float = 0.50146484375
    D_92: float = 0.0087738037109375
    D_93: float = 0.005344390869140625
    D_94: float = 0.005832672119140625
    R_24: float = 0.000843048095703125
    R_25: float = 0.000514984130859375
    D_96: float = 0.000522613525390625
    S_22: float = 0.2958984375
    S_23: float = 0.1328125
    S_24: float = 0.1376953125
    S_25: float = 0.9736328125
    S_26: float = 0.005733489990234375
    D_102: float = 0.0005321502685546875
    D_103: float = 0.0033512115478515625
    D_104: float = 0.0033016204833984375
    D_105: float = -1
    D_106: float = -1
    D_107: float = 0.005046844482421875
    B_36: float = 0.0096435546875
    B_37: float = 0.00576019287109375
    R_26: float = -1
    R_27: float = 1.0048828125
    B_38: float = 1.0
    D_108: float = -1
    D_109: float = 0.00995635986328125
    D_110: float = -1
    D_111: float = -1
    B_39: float = -1
    D_112: float = 1.0
    B_40: float = 0.05029296875
    S_27: float = -1
    D_113: float = 0.00811004638671875
    D_114: float = 1.0
    D_115: float = 0.386962890625
    D_116: float = 0.0
    D_117: float = 5.0
    D_118: float = 0.38037109375
    D_119: float = 0.37646484375
    D_120: float = 0.0
    D_121: float = 0.73583984375
    D_122: float = 0.580078125
    D_123: float = 0.002941131591796875
    D_124: float = 0.4580078125
    D_125: float = 0.0009655952453613281
    D_126: float = 1.0
    D_127: float = 0.0079345703125
    D_128: float = 0.9990234375
    D_129: float = 1.005859375
    B_41: float = 0.00917816162109375
    B_42: float = -1000
    D_130: float = 0.0063934326171875
    D_131: float = 0.008819580078125
    D_132: float = -1000
    D_133: float = 0.009674072265625
    R_28: float = 0.00156402587890625
    D_134: float = -1
    D_135: float = -1
    D_136: float = -1
    D_137: float = -1
    D_138: float = -1
    D_139: float = 0.0035648345947265625
    D_140: float = 0.007472991943359375
    D_141: float = 0.002410888671875
    D_142: float = -1
    D_143: float = 0.007717132568359375
    D_144: float = 0.005863189697265625
    D_145: float = 0.0014066696166992188


@app.get("/hello")
def welcome():
    """
    Hello
    :return: None
    """
    return {'message': 'Hello Data Scientist!'}


@app.post("/train")
def training():
    """
    Обучение модели, логирование метрик
    """
    pipeline_training(config_path=CONFIG_PATH)
    metrics = load_metrics(config_path=CONFIG_PATH)

    return {"metrics": metrics}


@app.post("/predict")
def prediction(file: UploadFile = File(...)):
    """
    Предсказание модели по данным из файла
    """
    result = pipeline_evaluate(config_path=CONFIG_PATH, data_path=file.file)
    assert isinstance(result, list), "Результат не соответствует типу list"
    return {"prediction": result[:5]}


@app.post("/predict_input")
def prediction_input(customer: InsuranceCustomer, config_path=CONFIG_PATH):
    """
    Предсказание модели по введенным данным
    """
    features = [
        customer.customer_ID,
        customer.S_2,
        customer.P_2,
        customer.D_39,
        customer.B_1,
        customer.B_2,
        customer.R_1,
        customer.S_3,
        customer.D_41,
        customer.B_3,
        customer.D_42,
        customer.D_43,
        customer.D_44,
        customer.B_4,
        customer.D_45,
        customer.B_5,
        customer.R_2,
        customer.D_46,
        customer.D_47,
        customer.D_48,
        customer.D_49,
        customer.B_6,
        customer.B_7,
        customer.B_8,
        customer.D_50,
        customer.D_51,
        customer.B_9,
        customer.R_3,
        customer.D_52,
        customer.P_3,
        customer.B_10,
        customer.D_53,
        customer.S_5,
        customer.B_11,
        customer.S_6,
        customer.D_54,
        customer.R_4,
        customer.S_7,
        customer.B_12,
        customer.S_8,
        customer.D_55,
        customer.D_56,
        customer.B_13,
        customer.R_5,
        customer.D_58,
        customer.S_9,
        customer.B_14,
        customer.D_59,
        customer.D_60,
        customer.D_61,
        customer.B_15,
        customer.S_11,
        customer.D_62,
        customer.D_63,
        customer.D_64,
        customer.D_65,
        customer.B_16,
        customer.B_17,
        customer.B_18,
        customer.B_19,
        customer.D_66,
        customer.B_20,
        customer.D_68,
        customer.S_12,
        customer.R_6,
        customer.S_13,
        customer.B_21,
        customer.D_69,
        customer.B_22,
        customer.D_70,
        customer.D_71,
        customer.D_72,
        customer.S_15,
        customer.B_23,
        customer.D_73,
        customer.P_4,
        customer.D_74,
        customer.D_75,
        customer.D_76,
        customer.B_24,
        customer.R_7,
        customer.D_77,
        customer.B_25,
        customer.B_26,
        customer.D_78,
        customer.D_79,
        customer.R_8,
        customer.R_9,
        customer.S_16,
        customer.D_80,
        customer.R_10,
        customer.R_11,
        customer.B_27,
        customer.D_81,
        customer.D_82,
        customer.S_17,
        customer.R_12,
        customer.B_28,
        customer.R_13,
        customer.D_83,
        customer.R_14,
        customer.R_15,
        customer.D_84,
        customer.R_16,
        customer.B_29,
        customer.B_30,
        customer.S_18,
        customer.D_86,
        customer.D_87,
        customer.R_17,
        customer.R_18,
        customer.D_88,
        customer.B_31,
        customer.S_19,
        customer.R_19,
        customer.B_32,
        customer.S_20,
        customer.R_20,
        customer.R_21,
        customer.B_33,
        customer.D_89,
        customer.R_22,
        customer.R_23,
        customer.D_91,
        customer.D_92,
        customer.D_93,
        customer.D_94,
        customer.R_24,
        customer.R_25,
        customer.D_96,
        customer.S_22,
        customer.S_23,
        customer.S_24,
        customer.S_25,
        customer.S_26,
        customer.D_102,
        customer.D_103,
        customer.D_104,
        customer.D_105,
        customer.D_106,
        customer.D_107,
        customer.B_36,
        customer.B_37,
        customer.R_26,
        customer.R_27,
        customer.B_38,
        customer.D_108,
        customer.D_109,
        customer.D_110,
        customer.D_111,
        customer.B_39,
        customer.D_112,
        customer.B_40,
        customer.S_27,
        customer.D_113,
        customer.D_114,
        customer.D_115,
        customer.D_116,
        customer.D_117,
        customer.D_118,
        customer.D_119,
        customer.D_120,
        customer.D_121,
        customer.D_122,
        customer.D_123,
        customer.D_124,
        customer.D_125,
        customer.D_126,
        customer.D_127,
        customer.D_128,
        customer.D_129,
        customer.B_41,
        customer.B_42,
        customer.D_130,
        customer.D_131,
        customer.D_132,
        customer.D_133,
        customer.R_28,
        customer.D_134,
        customer.D_135,
        customer.D_136,
        customer.D_137,
        customer.D_138,
        customer.D_139,
        customer.D_140,
        customer.D_141,
        customer.D_142,
        customer.D_143,
        customer.D_144,
        customer.D_145
    ]

    cols = [
        'customer_ID',
        'S_2',
        'P_2',
        'D_39',
        'B_1',
        'B_2',
        'R_1',
        'S_3',
        'D_41',
        'B_3',
        'D_42',
        'D_43',
        'D_44',
        'B_4',
        'D_45',
        'B_5',
        'R_2',
        'D_46',
        'D_47',
        'D_48',
        'D_49',
        'B_6',
        'B_7',
        'B_8',
        'D_50',
        'D_51',
        'B_9',
        'R_3',
        'D_52',
        'P_3',
        'B_10',
        'D_53',
        'S_5',
        'B_11',
        'S_6',
        'D_54',
        'R_4',
        'S_7',
        'B_12',
        'S_8',
        'D_55',
        'D_56',
        'B_13',
        'R_5',
        'D_58',
        'S_9',
        'B_14',
        'D_59',
        'D_60',
        'D_61',
        'B_15',
        'S_11',
        'D_62',
        'D_63',
        'D_64',
        'D_65',
        'B_16',
        'B_17',
        'B_18',
        'B_19',
        'D_66',
        'B_20',
        'D_68',
        'S_12',
        'R_6',
        'S_13',
        'B_21',
        'D_69',
        'B_22',
        'D_70',
        'D_71',
        'D_72',
        'S_15',
        'B_23',
        'D_73',
        'P_4',
        'D_74',
        'D_75',
        'D_76',
        'B_24',
        'R_7',
        'D_77',
        'B_25',
        'B_26',
        'D_78',
        'D_79',
        'R_8',
        'R_9',
        'S_16',
        'D_80',
        'R_10',
        'R_11',
        'B_27',
        'D_81',
        'D_82',
        'S_17',
        'R_12',
        'B_28',
        'R_13',
        'D_83',
        'R_14',
        'R_15',
        'D_84',
        'R_16',
        'B_29',
        'B_30',
        'S_18',
        'D_86',
        'D_87',
        'R_17',
        'R_18',
        'D_88',
        'B_31',
        'S_19',
        'R_19',
        'B_32',
        'S_20',
        'R_20',
        'R_21',
        'B_33',
        'D_89',
        'R_22',
        'R_23',
        'D_91',
        'D_92',
        'D_93',
        'D_94',
        'R_24',
        'R_25',
        'D_96',
        'S_22',
        'S_23',
        'S_24',
        'S_25',
        'S_26',
        'D_102',
        'D_103',
        'D_104',
        'D_105',
        'D_106',
        'D_107',
        'B_36',
        'B_37',
        'R_26',
        'R_27',
        'B_38',
        'D_108',
        'D_109',
        'D_110',
        'D_111',
        'B_39',
        'D_112',
        'B_40',
        'S_27',
        'D_113',
        'D_114',
        'D_115',
        'D_116',
        'D_117',
        'D_118',
        'D_119',
        'D_120',
        'D_121',
        'D_122',
        'D_123',
        'D_124',
        'D_125',
        'D_126',
        'D_127',
        'D_128',
        'D_129',
        'B_41',
        'B_42',
        'D_130',
        'D_131',
        'D_132',
        'D_133',
        'R_28',
        'D_134',
        'D_135',
        'D_136',
        'D_137',
        'D_138',
        'D_139',
        'D_140',
        'D_141',
        'D_142',
        'D_143',
        'D_144',
        'D_145'
    ]

    data = make_dataframe(cols, features, config_path)
    predictions = pipeline_evaluate(config_path=CONFIG_PATH, dataset=data)[0]
    result = ['Клиент вернет долг', 'Клиент не вернет долг']

    return result[predictions]


if __name__ == "__main__":
    # Запустите сервер, используя заданный хост и порт
    uvicorn.run(app, host="127.0.0.1", port=8002)
