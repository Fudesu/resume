/*
Найдите в таблице calendar_summary те доступные (available='t') объявления, у которых число отзывов от уникальных 
пользователей в таблице reviews выше среднего. Для этого с помощью конструкции WITH посчитайте среднее число уникальных 
reviewer_id из таблицы reviews на каждое жильё, потом проведите джойн таблиц calendar_summary и reviews по полю listing_id
(при этом из таблицы calendar_summary должны быть отобраны уникальные listing_id, отфильтрованные по правилу available='t'). 
Результат отфильтруйте так, чтобы остались только записи, у которых число отзывов от уникальных людей выше среднего.
Отсортируйте результат по возрастанию listing_id.
*/

WITH 
available_listings AS (
    SELECT listing_id
    FROM calendar_summary
    WHERE available = 't'
),
listing_reviewer_counts AS (
    SELECT  listing_id,
            COUNT(DISTINCT reviewer_id) as reviewer_number
    FROM reviews
    GROUP BY listing_id
),
avg_reviewer AS (
    SELECT  AVG(reviewer_number) as avg_reviewers
    FROM listing_reviewer_counts
)
SELECT  l.listing_id,
        r.reviewer_number
FROM available_listings as l
JOIN listing_reviewer_counts as r ON l.listing_id = r.listing_id
WHERE r.reviewer_number > (SELECT avg_reviewers FROM avg_reviewer)
ORDER BY l.listing_id
