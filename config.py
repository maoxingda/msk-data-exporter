import sys
from datetime import datetime, timezone

import yaml
import pytz


def main():
    # Data to be written to the YAML file
    start, end = sys.argv[1].split(' -> ')

    with open('topics') as f:
        topics = f.read()
    topics = topics.split('\n')
    topics = [topic for topic in topics if len(topic) > 0]

    conf = {
        "exporter": {
            "bootstrap-servers": [
                "b-2.bi-rdw-kafka.6pqqfj.c3.kafka.cn-northwest-1.amazonaws.com.cn:9092"
            ],
            "output": "/tmp/data.bin",
            "topics": topics,
            "offset-timstamp-ms": {
                "from": to_miliseconds(start),
                "to": to_miliseconds(end)
            }
        },
        "importer": {
            "bootstrap-servers": [
                "kafka:9092"
            ],
            "input": "/tmp/data.bin"
        }
    }

    # Writing the data to a YAML file
    with open('conf.yaml', 'w') as file:
        yaml.dump(conf, file)

    print("Data has been written to conf.yaml")


def to_miliseconds(beijing_time_str):
    # 定义北京时间时区
    beijing_tz = pytz.timezone('Asia/Shanghai')
    # 将字符串解析为datetime对象
    dt_beijing = datetime.strptime(beijing_time_str, '%Y/%m/%d %H:%M:%S')
    # 设置时区信息为北京时间
    dt_beijing = beijing_tz.localize(dt_beijing)
    # 转换为UTC时间
    dt_utc = dt_beijing.astimezone(timezone.utc)
    # 获取秒级时间戳
    timestamp_s = dt_utc.timestamp()
    # 转换为毫秒级时间戳
    timestamp_ms = int(timestamp_s * 1000)

    return timestamp_ms


if __name__ == '__main__':
    main()
