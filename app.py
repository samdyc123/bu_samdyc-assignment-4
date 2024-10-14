from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# 加载20个新闻组数据集
newsgroups_data = fetch_20newsgroups(subset='all')
documents = newsgroups_data.data

# 将文档转化为TF-IDF矩阵
vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
X = vectorizer.fit_transform(documents)

# 进行SVD降维
svd_model = TruncatedSVD(n_components=100)
X_reduced = svd_model.fit_transform(X)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided.'})

    # 将用户查询转化为TF-IDF向量，并在降维后的空间中表示
    query_vec = vectorizer.transform([query])
    query_reduced = svd_model.transform(query_vec)

    # 计算查询向量和文档向量之间的余弦相似度
    similarities = cosine_similarity(query_reduced, X_reduced)
    top_indices = np.argsort(similarities[0])[::-1][:5]  # 取前5个相似度最高的文档

    # 生成结果，包括文档内容和相似度得分
    results = [{'document': documents[i], 'similarity': similarities[0][i]} for i in top_indices]

    # 可视化相似度条形图
    labels = [f'Doc {i + 1}' for i in range(1, 6)]
    scores = [similarities[0][i] for i in top_indices]
    fig, ax = plt.subplots()
    ax.barh(labels, scores, color='lightblue')
    ax.set_xlabel('Cosine Similarity')
    ax.set_title('Top 5 Documents Similarity')

    # 将图表保存为内存中的PNG文件
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # 返回JSON数据，包括相似度最高的文档和图表的base64数据
    return jsonify({'results': results, 'graph': graph_url})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
