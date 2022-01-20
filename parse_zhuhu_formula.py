# -*- coding: utf-8 -*-
"""
功能：读取文件，批量解析知乎url中的公式，转换成LaTex格式
修改记录： 2022年1月20日 19:58:39 创建
"""

from urllib import parse
import re


ZHIHU_PATTERN = re.compile(r"!\[\[公式\]\]\(.+?\)")


def parse_url_2_formula(url):
    """

    :param url:
    :return:LaTex格式的字符串
    """

    # 解析url
    result = parse.urlparse(url)

    # 对请求部分解析成字典
    query_dict = parse.parse_qs(result.query)

    # 获取公式部分，返回的是列表格式
    formula_list = query_dict.get("tex", [])

    return "$ " + formula_list[0] + " $"


def get_formula(match_obj):
    """
    从匹配到的数据结构中找出url，并进行解析
    :param match_obj: re.Match数据结构
    :return: url
    """
    target_str = match_obj.group()
    left = target_str.rfind("(")
    url = target_str[left+1:-1]
    return parse_url_2_formula(url)


def create_bak_file_name(path):
    file_name = path[path.rfind("\\")+1:]
    bak_path = re.sub(file_name, f"bak_{file_name}", path)
    return bak_path


def patch_parse_file_content(file_path):
    # 创建备份文件名
    bak_path = create_bak_file_name(file_path)

    # 解析文件并保存
    with open(file_path, "r", encoding="utf-8") as input_file, \
         open(bak_path, "w", encoding="utf-8") as output_file:

        lines = input_file.read()
        # 替换成LaTex格式
        new = re.sub(ZHIHU_PATTERN, get_formula, lines)
        # 写入备份文件
        output_file.write(new)


if __name__ == "__main__":
    patch_parse_file_content(r"D:\zlb\httptunnel\a.md")