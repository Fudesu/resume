/*
Есть таблица анализов Analysis:

an_id — ID анализа;
an_name — название анализа;
an_cost — себестоимость анализа;
an_price — розничная цена анализа;
an_group — группа анализов.
Есть таблица групп анализов Groups:

gr_id — ID группы;
gr_name — название группы;
gr_temp — температурный режим хранения.
Есть таблица заказов Orders:

ord_id — ID заказа;
ord_datetime — дата и время заказа;
ord_an — ID анализа.
Далее мы будем работать с этими таблицами.

Задача 1.
Формулировка: вывести название и цену для всех анализов, которые продавались 5 февраля 2020 и всю следующую неделю.
Задача 2.
Формулировка: нарастающим итогом рассчитать, как увеличивалось количество проданных тестов каждый месяц каждого года с разбивкой по группе.
*/

-- Задача 1:

SELECT an_name as an_name, an_cost as an_cost
    FROM Analysis as an
    JOIN 
        (
            SELECT ord_datetime as ord_datetime
            FROM Orders
            WHERE ord_datetime BETWEEN '2020-02-05' AND '2020-02-12'
        ) as ord
    ON an.an_id = ord.ord_an
    ORDER_BY an.an_name

-- Задача 2

WITH sales as
(
    SELECT EXTRACT(YEAR FROM o.ord_datetime) as year,
           EXTRACT(MONTH FROM o.ord_datetime) as month,
           gr.gr_id as group_name,
           COUNT(ord_an) as cnt
    FROM Orders as o
    JOIN Analysis as a
    ON o.ord_an = a.an_id
    JOIN Groups as gr
    ON a.an_group = gr.gr_id
    GROUP BY EXTRACT(YEAR FROM o.ord_datetime) as year,
             EXTRACT(MONTH FROM o.ord_datetime) as month,
             gr.gr_id
)
SELECT s.year,
       s.month,
       s.group_name,
       SUM(s.cnt) OVER(PARTITION BY s.group_name ORDER BY s.year, s.month)
FROM sales as s
ORDER BY s.group_name, s.year, s.month
