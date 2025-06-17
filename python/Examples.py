# user_id - номер id пользователя
# name - ФИО пользователя
# age - возраст
# gender - гендер
# country - страна ['Россия', 'Казахстан', 'Беларусь', 'Сербия', 'Армения']
# registration_date - дата регистрации профиля
# last_login - дата последней авторизации
# total_actions - кол-во действий на сайте
# subscription_type - тип подписки Free/Premium
# avg_session_minutes - время проведённое на сайте
# platform - с какой платформы выполнялись действия ['Android', 'iOS', 'Web']
# order_amount - стоимость заказа
# order_status - статус заказа ['Completed', 'Refunded', 'Failed']
# product_category - категория продукта ['Электроника', 'Одежда', 'Продукты', 'Книги', 'Другое']
# refund_reason - причины возврата      'Электроника': ['Брак', 'Не соответствует описанию', 'Другое'],
#                                       'Одежда': ['Не подошел размер', 'Брак', 'Другое'],
#                                       'Продукты': ['Истек срок', 'Другое'],
#                                       'Книги': ['Другое'],
#                                       'Другое': ['Другое']

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("C:\\data.csv")
df['last_login'] = pd.to_datetime(df['last_login'])
df['registration_date'] = pd.to_datetime(df['registration_date'])

# Процент проваленных заказов.
percent_of_failure = round((df.loc[df.order_status == 'Failed'].order_status.count() / df.order_status.count()) * 100, 2)
# Процент возвратов.
percent_of_refund = round((df.loc[df.order_status == 'Refunded'].order_status.count() /
                     (df.loc[df.order_status == 'Completed'].order_status.count() + df.loc[df.order_status == 'Refunded'].order_status.count())) * 100, 2)

# Среднее и медиана возраста пользователей.
avg_age = df.age.mean()
median_age = df.age.median()

# Процент возвратов по категориям продукта и причинам возврата от общего кол-ва успешных(!Failed) заказов.
types_of_refund = df.loc[df.refund_reason != 'NaN'].groupby('product_category', as_index = False).refund_reason.value_counts().sort_values('count', ascending=False)
not_failed_categ = df.loc[df.order_status != 'Failed'].product_category.value_counts()
types_of_refund = types_of_refund.join(not_failed_categ, on='product_category', how = 'inner', lsuffix='_', rsuffix='_total')
types_of_refund['percent_of_refund_reason'] = round(types_of_refund.count_ / types_of_refund.count_total * 100, 2)
types_of_refund = types_of_refund.drop(columns = {'count_', 'count_total'}).sort_values('percent_of_refund_reason', ascending=False)

# Сумма потерянная кампанией по причине провала заказа.
lost_money = df.loc[df.order_status == 'Failed'].order_amount.sum()
percent_of_lost_money = lost_money / df.order_amount.sum() * 100

# Самое богатое имя.
name_group = df['name'].apply(lambda x: x.split(' ')[2] if x.startswith(('г-н', 'г-жа')) else x.split(' ')[1]) # избавление от лишних элементов
df_new = df
df_new['name'] = name_group
rich_name = df_new.groupby('name', as_index=False).order_amount.sum().sort_values('order_amount', ascending=False).head(1)

# ARPPU для бесплатных/премиум пользователей
avg_check_premium = df.groupby('subscription_type', as_index=False).order_amount.mean()

# Распределение возраста
sns.histplot(data = df.age) # 1 вариант
# df.age.hist(bins=33) # 2 вариант
plt.show()
