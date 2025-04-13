# -*- coding: utf‑8 -*-
"""
PySpark implementation of TextRank keyword extraction
faithful to Mihalcea & Tarau (2004).
"""
from pyspark import SparkConf, SparkContext
import re, os
from itertools import combinations
from nltk import pos_tag
from nltk.corpus import stopwords
import nltk

# 1. Spark 初始化 -------------------------------------------------------------
conf = SparkConf().setAppName("TextRankKeywordExtractor").setMaster("local[*]")
sc   = SparkContext(conf=conf)
nltk.download('averaged_perceptron_tagger_eng')

# 2. 预处理 -------------------------------------------------------------------
STOP = set(stopwords.words('english'))

TOKEN_RE = re.compile(r"[A-Za-z]{2,}")          # 仅保留长度≥2的英文词
WIN_SIZE  = 2                                   # 论文中推荐 2–3
DAMPING   = 0.85
MAX_ITER  = 30
MIN_DIFF  = 1e-4                                 # 收敛阈值

def tokenize_and_filter(line):
    """分词 + POS 过滤（只保留名词/形容词），同时去停用词."""
    tokens = TOKEN_RE.findall(line.lower())
    # NLTK 的 pos_tag 需要小批量；这里直接在 map 里调
    tagged  = pos_tag(tokens, tagset='universal')
    kept = [w for w, t in tagged if t.startswith('NN') or t.startswith('JJ')]
    return kept

# sentences = sc.textFile("/data/text_corpus.txt") \
#               .map(tokenize_and_filter) \
#               .filter(lambda x: x)               # 去掉空行

# 将原始文本在 driver 上读取 & 处理 POS
lines = sc.textFile("/data/text_corpus.txt").collect()

processed = []
for line in lines:
    tokens = TOKEN_RE.findall(line.lower())
    tagged = pos_tag(tokens)  # 不再传 tagset='universal'
    kept = [w for w, t in tagged if t.startswith('NN') or t.startswith('JJ')]
    if kept:
        processed.append(kept)

sentences = sc.parallelize(processed)


# 3. 构建无向加权图 -----------------------------------------------------------
def window_pairs(tokens, window=WIN_SIZE):
    """在给定窗口内产生无向词对 (两边都记一份)"""
    for i in range(len(tokens)):
        for w1, w2 in combinations(tokens[i:i+window], 2):
            if w1 != w2:
                yield ((w1, w2), 1)
                yield ((w2, w1), 1)              # 对称边

edges = (sentences.flatMap(window_pairs)
                   .reduceByKey(lambda x, y: x + y))      # 边权 = 共现次数

# 4. 生成邻接表  --------------------------------------------------------------
adj = (edges.map(lambda x: (x[0][0], (x[0][1], x[1])))     # (src, (dst, weight))
             .groupByKey()
             .mapValues(list)
             .cache())

# 5. TextRank 迭代  -----------------------------------------------------------
ranks = adj.mapValues(lambda _: 1.0)                       # 初始化为 1

for _ in range(MAX_ITER):
    # 计算每个节点出边权重之和，用于归一化
    weight_sums = adj.mapValues(lambda nbrs: sum(w for _, w in nbrs))
    weight_sums = sc.broadcast(dict(weight_sums.collect()))

    contribs = (adj.join(ranks)                             # (word, (nbrs, rank))
                   .flatMap(lambda x: [
                       (nbr, (x[1][1] * w) / weight_sums.value[x[0]])
                       for nbr, w in x[1][0] if weight_sums.value[x[0]] > 0
                   ]))

    new_ranks = contribs.reduceByKey(lambda a, b: a + b) \
                        .mapValues(lambda r: (1 - DAMPING) + DAMPING * r)

    # 判断收敛
    diff = (ranks.join(new_ranks)
                 .mapValues(lambda x: abs(x[0] - x[1]))
                 .values()
                 .sum())
    ranks = new_ranks
    if diff < MIN_DIFF:
        break

# 6. 选取前 N 个关键词（N = 节点数的 1/3，论文中的启发式） ---------------------
node_cnt = ranks.count()
TOP_N    = max(5, node_cnt // 3)

top_keywords = (ranks.takeOrdered(TOP_N, key=lambda x: -x[1]))

# 7. 多词关键短语重组 ----------------------------------------------------------
#   先把原文广播下来，标出已选关键词，最后按相邻位置合并
all_text = " ".join(sentences.flatMap(lambda x: x).collect())
tokens   = TOKEN_RE.findall(all_text.lower())
positions = {}
for idx, tok in enumerate(tokens):
    positions.setdefault(tok, []).append(idx)

chosen = set(k for k, _ in top_keywords)

# 根据位置把相邻的选中词合并
phrases = []
skip = set()
for tok in tokens:
    if tok in skip or tok not in chosen:
        continue
    pos_list = positions[tok]
    for pos in pos_list:
        phrase = [tok]
        nxt = pos + 1
        while nxt < len(tokens) and tokens[nxt] in chosen:
            phrase.append(tokens[nxt])
            skip.add(tokens[nxt])
            nxt += 1
        phrases.append(" ".join(phrase))

print("== Top keywords ==")
for p in phrases[:TOP_N]:
    print(p)

sc.stop()