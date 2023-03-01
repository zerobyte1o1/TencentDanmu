import os
import sys

import openpyxl
import requests
import yaml


def tencentdanmu(set_length, target_id, setname=None):
    wb = openpyxl.Workbook()
    sheet = wb.active
    headers = {
        'User-Agent': 'Googlebot'
    }
    list_content = []
    for i in range(30, int(set_length) * 60, 30):
        nowtime = i * 1000
        url = f"https://dm.video.qq.com/barrage/segment/{target_id}/t/v1/{nowtime - 30000}/{nowtime}"
        print('正在获取弹幕：' + url)
        res = requests.get(url, headers=headers).json(strict=False)
        list_content.extend([i['content'] for i in res['barrage_list']])
    # for i in list_content:
    #     sheet.append([i])
    results_url = os.path.abspath("results")
    result_abs = os.path.join(results_url, f'{setname}.txt')
    # wb.save(result_abs)
    # comments_file_path = 'lrcs_comments.txt'

    # 获取comments中的弹幕信息并且写入指定路径

    with open(result_abs, 'w+', encoding='utf-8')as fin:
        for comment in list_content:
            fin.write(comment + '\n')



def read_yaml():
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "config.yaml")
    config = yaml.safe_load(open(configPath))
    return config


if __name__ == '__main__':
    if len(sys.argv)==1:
        for item in read_yaml():
            tencentdanmu(item['time'], item['key'], item['name'])
    else:
        tencentdanmu(sys.argv[3],sys.argv[2],sys.argv[1])