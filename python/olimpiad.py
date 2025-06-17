# Рассмотрим таблицы результатов школьной олимпиады, которая проходит сразу в нескольких регионах в несколько дней:
# 
# регионы пронумерованы числами от 1 до r;
# дни олимпиады пронумерованы числами от 1 до d;
# задачи в i-м из дней пронумерованы числа от 1 до pi;
# все участники олимпиады в ri-м регионе пронумерованы числами от 1 до ui
# и имеют логин user_ri_id.
# Общие результаты олимпиады представлены в файле "name_00_00.csv".
# 
# Постройте таблицы результатов по регионам и дням отдельно. Найдите регион и тур олимпиады, в котором у участника на 10-м месте больше всего баллов.
# 
# Отсортируйте результаты по убыванию суммы баллов, если несколько участников получили одинаковые суммы, то их стоит упорядочить по логину в лексикографическом порядке.
# Обратите внимание, что некоторые ячейки в итоговом .csv файле должны быть пустыми.

import pandas as pd
import os

def olimpiad():
  df_score = pd.read_csv("C:\\dataframes\\data-to-split\\test_00_00.csv")
  df1 = pd.read_csv("C:\\dataframes\\data-to-split\\train_00_00.csv")
  df2 = pd.read_csv("C:\\dataframes\\data-to-split\\train_02_01.csv")
  # print(df_score, '\n', df1, '\n', df2)
  
  df_score['region'] = df_score.username.apply(lambda x: x.split('_')[1])
  df_ = []
  for region in df_score.region.unique():
      try:
          df_.append({(region + '_01') : int(df_score.groupby('region', as_index = False)
              .get_group(region)
              .reset_index()
              .iloc[:, 2:6]
              .sum(axis = 1)
              .sort_values(ascending=False)
              .reset_index()
              .iloc[9,1])})
      except:
          pass
      try:
          df_.append({(region + '_02') : int(df_score.groupby('region', as_index = False)
              .get_group(region)
              .reset_index()
              .iloc[:, 6:10]
              .sum(axis = 1)
              .sort_values(ascending=False)
              .reset_index()
              .iloc[9,1])})
      except:
          pass
  df_07_02 = df_score.groupby('region', as_index = False).get_group('07').reset_index().iloc[:, 6:10].astype('Int64')
  df_07_02['score'] = df_07_02.sum(axis =1, numeric_only=True)
  df_join = pd.DataFrame(df_score.groupby('region', as_index = False).get_group('07').username.reset_index(drop = True))
  df_07_02 = df_join.join(df_07_02).sort_values(by=['score', 'username'], ascending=[False, True], ignore_index = True)
  df_07_02.to_csv('C:\\dataframes\\data-to-split\\test_07_02.csv', index = False)

# Жюри олимпиады решили построить альтернативную таблицу результатов: для каждого из участников результатом отдельного тура 
# будем считать значение наибольшего из результатов по отдельной задаче этого тура. Итогом участия в олимпиаде будем сумма результатов по турам.
# 
# Для получения итогового файла требуется выполнить следующие действия:
# 
# Заменить все отсутствующие значения нулями.
# Удалить колонку score.
# Для каждого тура олимпиады добавить колонку score_d, где d номер тура олимпиады.
# Добавить колонку score с суммой результатов по всем дням.
# Отсортировать результаты по убыванию суммы баллов, если несколько участников получили одинаковые суммы, 
# то их стоит упорядочить по логину в лексикографическом порядке.
def olimpiad_fill():
  df = pd.read_csv("C:\\dataframes\\data-to-fill\\test_00_00.csv")
  df1 = pd.read_csv("C:\\dataframes\\data-to-fill\\train_00_00.csv")
  df2 = pd.read_csv("C:\\dataframes\\data-to-fill\\train_filled.csv")
  # print(df1.head(), '\n', df2.head())
  # print(df.head())
  
  df = df.drop(columns = ['score'])
  
  
  print(df.head())
  print(df.filter(like='1_').columns)
  print(df.filter(like='_1').columns.nunique())
  df = df.fillna(0)
  for day in range(df.filter(like='_1').columns.nunique()):
      df['score_' + str(day+1)] = df.filter(like=(str(day+1) + '_')).apply(lambda x: x.max(), axis = 1)
  df['score'] = df.filter(like = 'score_').sum(axis = 1)
  df = df.sort_values(['score', 'username'], ascending=[False, True]).reset_index(drop=True)
  print(df)
  df.to_csv("C:\\dataframes\\data-to-fill\\test_filled.csv", index = False)
# Результаты олимпиады di-го дня в rj-м регионе представлены в файле "name_rj_di.csv".
# Постройте общую таблицу результатов по всем регионам и по всем дням олимпиады.
# Отсортируйте результаты по убыванию суммы баллов, если несколько участников получили одинаковые суммы,
# то их стоит упорядочить по логину в лексикографическом порядке.
def olimpiad_merge():
    dir = os.listdir("C:\\dataframes\\data-to-merge\\test")
    df_left = pd.DataFrame({'username':[]})
    df_right = pd.DataFrame({'username': []})
    for part in dir[::2]:
        df_to_merge = pd.read_csv(f'C:\\dataframes\\data-to-merge\\test\\{part}')
        df_left = df_left.merge(df_to_merge, how = 'outer')
    for part in dir[1::2]:
        df_to_merge = pd.read_csv(f'C:\\dataframes\\data-to-merge\\test\\{part}')
        df_right = df_right.merge(df_to_merge, how = 'outer')
    df_all = df_left.merge(df_right, how = 'inner', on = 'username')
    df_all = df_all.rename(columns = {'score_y' : 'score'})
    df_all['score'] = df_all.score + df_all.score_x
    df_all = df_all.drop(columns = {'score_x'}).sort_values(['score', 'username'], ascending= [False, True]).reset_index(drop= True)
    df_all.to_csv('C:\\dataframes\\data-to-merge\\test_00_00.csv', index = False)

  
