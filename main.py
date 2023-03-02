import os
import sys

import requests
import yaml
import jieba
import wordcloud
from openpyxl import load_workbook
from snownlp import SnowNLP
import jieba.analyse as analyse


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
        for i in t:
            if i == '哈' or i == 'ha':
                t = t.replace(i, '')

        keywords_top20 = analyse.extract_tags(t, withWeight=True, topK=20)
        print('top20关键词及权重：')
        print(keywords_top20)
        sentiment_analyse(t, setname, keywords_top20)
        # word_list = jieba.lcut_for_search(t)
        # new_word_list = ' '.join(word_list)

        import platform
        if 'Windows' == platform.system():
            w = wordcloud.WordCloud(width=2000,
                                    height=1400,
                                    font_path="msyh.ttc")
        else:
            w = wordcloud.WordCloud(width=2000,
                                    height=1400,
                                    font_path="/System/Library/Fonts/PingFang.ttc")
        w.generate(t)
        w.to_file(os.path.join(os.path.abspath("yuntu"), f'{setname}.png'))


def sentiment_analyse(v_cmt_list, setname, keywords_top20):
    """
    情感分析打分
    :param v_cmt_list: 需要处理的评论列表
    :return:
    """
    score_list = []  # 情感评分值
    tag_list = []  # 打标分类结果
    pos_count = 0  # 计数器-积极
    neg_count = 0  # 计数器-消极
    for comment in v_cmt_list:
        tag = ''
        sentiments_score = SnowNLP(comment).sentiments
        if sentiments_score < 0.4:
            tag = '消极'
            neg_count += 1
        else:
            tag = '积极'
            pos_count += 1
        score_list.append(sentiments_score)  # 得分值
        tag_list.append(tag)  # 判定结果

    print('消极评价占比：', round(neg_count / (pos_count + neg_count), 4))
    wb = load_workbook(os.path.join(os.path.abspath('emotions'), "情绪分析.xlsx"))
    ws = wb['Sheet1']
    ws.append([setname, "积极评价", round(pos_count / (pos_count + neg_count), 4)])
    ws.append([setname, "消极评价", round(neg_count / (pos_count + neg_count), 4), str(keywords_top20)])
    wb.save(os.path.join(os.path.abspath('emotions'), "情绪分析.xlsx"))
    print('情感分析结果已生成：情感分析')


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
