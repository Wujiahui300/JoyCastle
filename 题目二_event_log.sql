-- 题目二：event_log 表查询

SELECT COUNT(1) AS user_count
FROM (
    SELECT user_id
    FROM event_log
    WHERE event_timestamp >= UNIX_TIMESTAMP('2020-09-01 00:00:00')  
      AND event_timestamp < UNIX_TIMESTAMP('2020-10-01 00:00:00')
    GROUP BY user_id
    HAVING COUNT(1) >= 1000 AND COUNT(1) < 2000
) AS t;
