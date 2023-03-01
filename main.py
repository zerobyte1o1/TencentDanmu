import os
import sys

import requests
import yaml
import jieba
import wordcloud


def tencentdanmu(set_length, target_id, setname=None):
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
    results_url = os.path.abspath("results")
    result_abs = os.path.join(results_url, f'{setname}.txt')

    with open(result_abs, 'w+', encoding='utf-8')as fin:
        for comment in list_content:
            fin.write(comment + '\n')

    with open(result_abs, encoding='utf-8') as f:
        t = f.read()
        word_list = jieba.lcut_for_search(t)
        new_word_list = ' '.join(word_list)
        import platform
        if 'Windows' == platform.system():
            w = wordcloud.WordCloud(width=2000,
                                    height=1400,
                                    font_path="msyh.ttc")
        else:
            w = wordcloud.WordCloud(width=2000,
                                    height=1400,
                                    font_path="/System/Library/Fonts/PingFang.ttc")
        w.generate(new_word_list)
        w.to_file(os.path.join(os.path.abspath("yuntu"), f'{setname}.png'))
    # with open(result_abs,'w+', encoding='utf-8') as file:
    #     comment_text = file.read()
    #     print(comment_text)
    #     # 使用jieba精确模式，句子最精确地切开，适合文本分析
    #     word_list = jieba.lcut_for_search(comment_text)
    #     new_word_list = ' '.join(word_list)
    #     print(new_word_list)
    #     file.write(new_word_list)


def read_yaml():
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "config.yaml")
    config = yaml.safe_load(open(configPath))
    return config


if __name__ == '__main__':
    if len(sys.argv) == 1:
        for item in read_yaml():
            tencentdanmu(item['time'], item['key'], item['name'])
    else:
        tencentdanmu(sys.argv[3], sys.argv[2], sys.argv[1])
