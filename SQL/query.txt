/* Определить cреднее время ожидания (в минутах) принятия кампании по дням. Допустим, у кампании 5012025 пришло отклонение в 2024-10-07 12:46:29 и затем пришло принятие в 2024-10-07 15:12:49. Время ожидания 2 часа 26 минут 20 секунд.

Есть таблица logs следующего вида:

logs (
    campaign_id INTEGER NOT NULL,
    verdict TEXT NOT NULL,
    verdict_time TEXT NOT NULL
);
Где campaign_id — идентификатор рекламной кампании, verdict — вердикт модерации, может быть равен только "Yes" или "No", verdict_time — время получения вердикта в формате YYYY-MM-DD hh:mm:ss.

ПРИМЕР:
campaign_id  verdict  verdict_time
2  No  2025-01-02 14:28:10
1  No  2025-01-02 18:52:57
2  Yes  2025-01-03 00:47:40
1  No  2025-01-03 01:12:32
1  Yes  2025-01-03 05:10:38
1  Yes  2025-01-03 09:19:44
2  No  2025-01-04 11:49:49
1  Yes  2025-01-04 13:29:01
2  No  2025-01-04 16:01:37
1  No  2025-01-04 20:35:31

ОТВЕТ:
field_date  avg_wait_time
2025-01-02  620
2025-01-03  238
*/

SELECT  TO_CHAR(previous_verdict_time::DATE, 'YYYY-MM-DD') AS field_date,   
        ROUND(EXTRACT(EPOCH FROM (TO_TIMESTAMP(verdict_time, 'YYYY-MM-DD HH24:MI:SS') - 
                            TO_TIMESTAMP(previous_verdict_time, 'YYYY-MM-DD HH24:MI:SS'))) / 60) AS avg_wait_time
FROM (SELECT    *, 
                LAG(verdict) OVER (PARTITION BY campaign_id ORDER BY verdict_time) AS previous_verdict,
                LAG(verdict_time) OVER (PARTITION BY campaign_id ORDER BY verdict_time) AS previous_verdict_time
      FROM logs
      )
WHERE verdict = 'Yes' AND previous_verdict = 'No'
GROUP BY field_date
ORDER BY field_date
