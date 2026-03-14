-- 题目二：event_log 表查询
-- 表结构：user_id, event_timestamp
-- 查询有多少用户在 2020年9月 开启关卡数 >= 1000 且 < 2000

SELECT COUNT(*) AS user_count
FROM (
    SELECT user_id
    FROM event_log
    WHERE event_timestamp >= UNIX_TIMESTAMP('2020-09-01 00:00:00')  
      AND event_timestamp < UNIX_TIMESTAMP('2020-10-01 00:00:00')   -- 2020年10月1日 00:00:00 UTC
    GROUP BY user_id
    HAVING COUNT(*) >= 1000 AND COUNT(*) < 2000
) AS t;
