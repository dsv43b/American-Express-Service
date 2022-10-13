"""
Программа: Тренировка данных
Версия: 1.0
"""

import optuna
from catboost import CatBoostClassifier

from optuna import Study

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np
from ..data.split_dataset import get_train_test_data
from ..train.metrics import save_metrics, amex_metric


class Amex_metric_cat:
    '''Amex метрика для CatBoost'''

    def is_max_optimal(self):
        return True

    def evaluate(self, approxes, target, weight):
        return amex_metric(target, approxes[0]), 0

    def get_final_error(self, error, weight):
        return error


def objective(
        trial,
        data_x: pd.DataFrame,
        data_y: pd.Series,
        cat_features: list,
        n_folds: int = 5,
        random_state: int = 25
) -> np.array:
    """
    Целевая функция для поиска параметров
    :param trial: кол-во trials
    :param data_x: данные объект-признаки
    :param data_y: данные с целевой переменной
    :param cat_features: список категориальных данных
    :param n_folds: кол-во фолдов
    :param random_state: random_state
    :return: среднее значение метрики по фолдам
    """
    param_grid = {
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float("learning_rate", 0.001, 0.5, log=True),
        'n_estimators': trial.suggest_categorical("n_estimators", [1000]),
        # 'max_bin': trial.suggest_int('max_bin', 200, 400),
        # 'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 1, 300),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 0.0001, 1.0, log=True),
        # 'subsample': trial.suggest_float('subsample', 0.1, 0.8),
        'random_seed': random_state,
        'loss_function': 'Logloss',
        'eval_metric': Amex_metric_cat(),
        # 'task_type': 'GPU',
        # 'bootstrap_type': 'Poisson',
        'cat_features': cat_features
    }

    cv_folds = StratifiedKFold(
        n_splits=n_folds, shuffle=True, random_state=random_state
    )
    cv_predicts = np.empty(n_folds)

    for idx, (train_idx, test_idx) in enumerate(cv_folds.split(data_x, data_y)):
        x_train, x_test = data_x.iloc[train_idx], data_x.iloc[test_idx]
        y_train, y_test = data_y.iloc[train_idx], data_y.iloc[test_idx]

        model = CatBoostClassifier(**param_grid, silent=True)
        model.fit(
            x_train,
            y_train,
            eval_set=[(x_test, y_test)],
            early_stopping_rounds=100,
            verbose=False
        )
        predict = model.predict_proba(x_test)[:, 1]
        cv_predicts[idx] = amex_metric(y_test, predict)
    return np.mean(cv_predicts)


def find_optimal_params(
        data_train: pd.DataFrame, data_test: pd.DataFrame, cat_features: list, **kwargs
) -> Study:
    """
    Пайплайн для тренировки модели
    :param data_train: датасет train
    :param data_test: датасет test
    :param cat_features: список категориальных данных
    :return: [CatBoostClassifier tuning, Study]
    """
    x_train, x_test, y_train, y_test = get_train_test_data(
        data_train=data_train, data_test=data_test, target=kwargs["target_column"]
    )
    study = optuna.create_study(direction="maximize", study_name="CatBoost")
    function = lambda trial: objective(
        trial, x_train, y_train, cat_features, kwargs["n_folds"], kwargs["random_state"]
    )
    study.optimize(function, n_trials=kwargs["n_trials"], show_progress_bar=True)
    return study


def train_model(
        data_train: pd.DataFrame,
        data_test: pd.DataFrame,
        study: Study,
        cat_features: list,
        target: str,
        metric_path: str,
) -> CatBoostClassifier:
    """
    Обучение модели на лучших параметрах
    :param data_train: тренировочный датасет
    :param data_test: тестовый датасет
    :param study: study optuna
    :param cat_features: список категориальных данных
    :param target: название целевой переменной
    :param metric_path: путь до папки с метриками
    :return: CatBoostClassifier
    """

    # Получение данных
    x_train, x_test, y_train, y_test = get_train_test_data(
        data_train=data_train, data_test=data_test, target=target
    )

    # Тренировка с отимальными параметрами
    clf = CatBoostClassifier(**study.best_params, eval_metric=Amex_metric_cat(), cat_features=cat_features)
    clf.fit(x_train, y_train, eval_set=[(x_test, y_test)], early_stopping_rounds=100, verbose=False)

    # Сохранение метрик
    save_metrics(data_x=x_test, data_y=y_test, model=clf, metric_path=metric_path)
    return clf
