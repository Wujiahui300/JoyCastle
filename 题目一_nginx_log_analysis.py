"""
题目一：Nginx 服务器日志分析
"""

import re
import sys
from collections import defaultdict
from urllib.parse import urlparse
from datetime import datetime


# Nginx 日志正则表达式
LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d+)\s+(?P<size>\S+)\s+'
    r'"(?P<referer>[^"]*)"\s+"(?P<user_agent>[^"]*)"'
)


def parse_log_line(line: str):
    """解析单行 Nginx 日志"""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return match.groupdict()


def count_https_domain1_requests(log_file_path: str):
    ## 统计 HTTPS 请求中以 domain1.com 为域名的数量
    count = 0

    referer_pattern = re.compile(r'\d+\s+\S+\s+"([^"]*)"')
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = referer_pattern.search(line)
            if match:
                referer = match.group(1)
                if referer.startswith('https://'):
                    try:
                        parsed = urlparse(referer)
                        if parsed.netloc and 'domain1.com' in parsed.netloc:
                            count += 1
                    except Exception:
                        pass
    return count


def success_ratio_by_date(log_file_path: str, date: str):
    """
    给定日期 date ，计算当日 UTC 时间所有请求中成功的比例   
    HTTP 成功状态码在200-299之间
    """
    total = 0
    success = 0
    target_date = None
    
    for fmt in ['%Y-%m-%d', '%d/%b/%Y']:
        try:
            target_date = datetime.strptime(date, fmt).date()
            break
        except ValueError:
            continue
    
    if target_date is None:
        raise ValueError(f"无法解析日期: {date}，请使用 YYYY-MM-DD 或 DD/Mon/YYYY 格式")
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed = parse_log_line(line)
            if not parsed:
                continue
            # 解析时间戳 [28/Feb/2019:13:17:10 +0000]
            ts_str = parsed.get('timestamp', '')
            try:
                log_dt = datetime.strptime(ts_str.split()[0], '%d/%b/%Y:%H:%M:%S')
                if log_dt.date() != target_date:
                    continue
            except (ValueError, IndexError):
                continue
            
            total += 1
            status = int(parsed.get('status', 0))
            if 200 <= status < 300:
                success += 1
    
    if total == 0:
        return 0.0
    return success / total


def main():
    
    log_file = sys.argv[1] if len(sys.argv) > 1 else 'access.log'
    date_arg = sys.argv[2] if len(sys.argv) > 2 else '2019-02-28'
    
    count = count_https_domain1_requests(log_file)
    print(f"1. HTTPS 请求中以 domain1.com 为域名的数量: {count}")
    ratio = success_ratio_by_date(log_file, date_arg)
    print(f"2. {date_arg} 当日请求成功比例: {ratio:.2%}")


if __name__ == '__main__':
    main()
