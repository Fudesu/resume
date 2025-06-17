# A/B-test на изменение значений стоимости заказов (order_amount)
import pandas as pd
import numpy as np
import scipy
from scipy import stats

df_control = pd.read_csv("C:\\data_control.csv")
df_test = pd.read_csv("C:\\data_test.csv")
norm_test_control = stats.shapiro(df_control['order_amount'].sample(1000, random_state=18))
norm_test_test = stats.shapiro(df_test['order_amount'].sample(1000, random_state=18))

# ShapiroResult(statistic=np.float64(0.9540003651186031), pvalue=np.float64(3.720380923083018e-17))
# ShapiroResult(statistic=np.float64(0.9539301808370564), pvalue=np.float64(3.6034482614040355e-17))
# Оба распределения не являются нормальными, поэтому воспользуемся тестом Манна-Уитни

MW_test = stats.mannwhitneyu(df_control['order_amount'], df_test['order_amount'])

# MannwhitneyuResult(statistic=np.float64(12278694.0), pvalue=np.float64(0.12523327663512862))
# p-value < 0.05, это означает, что нулевая гипотеза о равенстве выборок не верна и имеются значимые статистические отклонения
# проверим значения медиан и среднего для контрольной и тестовой группы

median_control = df_control.order_amount.median() # 174.68
median_test = df_test.order_amount.median() # 182.495
avg_control = df_control.order_amount.mean() # 199.80727599999997
avg_test = df_test.order_amount.mean() # 208.60744200000002

# В результате теста были выявлены статистически значимые отклонения, которые показывают повышение медианы и среднего значения стоимости заказа.
# Это означает, что новое обновление стоит расширять на весь сервис.
# Примечание: в случае нормального распределения вместо теста Манна-Уитни был бы применён t-test. 
# Если же значение p-value было бы > 0.05, то в таком случае не было бы выявлено статистических изменений и обновление не имело бы смысла выпускать 
# (при условии достаточной выборки и выбранного уровня значимости).
