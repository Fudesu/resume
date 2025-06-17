-- Какие три клиента принесли больше всего выручки за третью неделю года?

SELECT bracelet_id
FROM pizza
WHERE EXTRACT(WEEK from date) = 3
GROUP BY bracelet_id
ORDER BY SUM(price * quantity) DESC
LIMIT 3

-- Вычислить ARPPU на каждый день января.

SELECT EXTRACT(day from date), SUM(quantity*price)/COUNT(DISTINCT(bracelet_id)) as ARPPU
FROM pizza
WHERE EXTRACT(month from date) = 1
GROUP BY EXTRACT(day from date)

-- Определить CR на 1000 показов на каждый месяц, исключив список id.

SELECT DATE_TRUNC('month', date), COUNT(DISTINCT(bracelet_id)) / 1000.0 as CR
FROM pizza
WHERE bracelet_id NOT IN(145738, 145759, 145773, 145807, 145815, 145821, 145873, 145880)
GROUP BY DATE_TRUNC('month', date)
ORDER BY DATE_TRUNC('month', date)

-- Вывести продукты (таблица Products), которые не продавались (таблица Sales).

SELECT product_id, product_name 
FROM Products 
WHERE product_id NOT IN (SELECT DISTINCT product_id FROM Sales)

-- Вывести детали продажи (таблица Sales) продуктов, в названии которых есть слово 'Smart' (таблица Products).

SELECT s.sale_id, p.product_name, s.total_price 
FROM Sales s 
JOIN Products p ON s.product_id = p.product_id 
WHERE p.product_name LIKE '%Smart%'

-- Вывести накопительную сумму total_volume для регионов 'NewYork', 'LosAngeles' по годам для 'organic' авокадо.

SELECT
    region,
    date,
    total_volume,
    SUM(total_volume) OVER (PARTITION BY region, DATE_TRUNC('year', date) ORDER BY date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_volume
FROM
    avocado
WHERE
    region in ('NewYork', 'LosAngeles') AND type = 'organic'
ORDER BY region DESC, date ASC
