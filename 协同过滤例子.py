import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ===========================
# 模拟数据库
# ===========================
database = {
    'users': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'items': ['Laptop', 'Phone', 'Tablet', 'Headphones'],
    
    # 用户对商品的评分 (0 表示未评分)
    'ratings': {
        'Alice': {'Laptop': 5, 'Phone': 3, 'Tablet': 0, 'Headphones': 1},
        'Bob': {'Laptop': 4, 'Phone': 0, 'Tablet': 0, 'Headphones': 1},
        'Charlie': {'Laptop': 1, 'Phone': 1, 'Tablet': 0, 'Headphones': 5},
        'David': {'Laptop': 0, 'Phone': 0, 'Tablet': 5, 'Headphones': 4},
        'Eve': {'Laptop': 0, 'Phone': 3, 'Tablet': 4, 'Headphones': 0},
    },
    
    # 商品的特征 (例如：电子、通信、音频)
    'item_features': {
        'Laptop': [1, 0, 1],       # 电子+办公
        'Phone': [0, 1, 0],        # 通信
        'Tablet': [1, 1, 0],       # 电子+通信
        'Headphones': [0, 0, 1],   # 音频
    }
}

# ===========================
# 构建用户-商品评分矩阵
# ===========================
def build_ratings_matrix(database):
    """
    根据数据库构建用户-商品评分矩阵。
    """
    users = database['users']
    items = database['items']
    
    # 初始化评分矩阵，矩阵大小为 (用户数量, 商品数量)
    ratings_matrix = np.zeros((len(users), len(items)))
    
    # 填充评分矩阵
    for i, user in enumerate(users):
        for j, item in enumerate(items):
            ratings_matrix[i, j] = database['ratings'][user][item]
    
    return ratings_matrix

# ===========================
# 构建商品特征矩阵
# ===========================
def build_item_features_matrix(database):
    """
    根据数据库构建商品特征矩阵。
    """
    items = database['items']
    
    # 提取商品的特征向量
    features_matrix = np.array([database['item_features'][item] for item in items])
    return features_matrix

# ===========================
# 协同过滤推荐系统
# ===========================
def collaborative_filtering_recommend(user_name, database, top_n=2):
    """
    基于协同过滤的推荐系统。
    """
    # 构建评分矩阵
    ratings_matrix = build_ratings_matrix(database)
    
    # 计算商品之间的相似度矩阵（基于评分的余弦相似度）
    item_similarity = cosine_similarity(ratings_matrix.T)
    
    # 获取用户的评分记录
    user_id = database['users'].index(user_name)
    user_ratings = ratings_matrix[user_id]
    
    # 计算推荐得分，基于商品相似度和用户的评分
    scores = item_similarity.dot(user_ratings)
    
    # 对于用户已经评分的商品，得分设为 0，避免重复推荐
    scores[user_ratings > 0] = 0
    
    # 返回得分最高的商品
    recommended_items = np.argsort(scores)[::-1][:top_n]
    return [database['items'][i] for i in recommended_items]

# ===========================
# 基于内容的推荐系统
# ===========================
def content_based_recommend(user_name, database, top_n=2):
    """
    基于内容的推荐系统。
    """
    # 构建评分矩阵
    ratings_matrix = build_ratings_matrix(database)
    
    # 构建商品特征矩阵
    item_features_matrix = build_item_features_matrix(database)
    
    # 计算商品之间的相似度矩阵（基于商品特征的余弦相似度）
    item_similarity = cosine_similarity(item_features_matrix)
    
    # 获取用户的评分记录
    user_id = database['users'].index(user_name)
    user_ratings = ratings_matrix[user_id]
    
    # 计算用户的兴趣向量（基于用户评分过的商品的相似度）
    user_profile = np.sum(item_similarity[user_ratings > 0], axis=0)
    
    # 对于用户已经评分的商品，得分设为 0，避免重复推荐
    user_profile[user_ratings > 0] = 0
    
    # 返回得分最高的商品
    recommended_items = np.argsort(user_profile)[::-1][:top_n]
    return [database['items'][i] for i in recommended_items]

# ===========================
# 混合推荐系统
# ===========================
def hybrid_recommend(user_name, database, alpha=0.5, top_n=2):
    """
    混合推荐系统：结合协同过滤和基于内容的推荐。
    alpha: 协同过滤和基于内容的权重，范围 [0, 1]。
    """
    # 构建评分矩阵
    ratings_matrix = build_ratings_matrix(database)
    
    # 构建商品特征矩阵
    item_features_matrix = build_item_features_matrix(database)
    
    # 计算协同过滤的商品相似度矩阵
    item_similarity_cf = cosine_similarity(ratings_matrix.T)
    
    # 计算基于内容的商品相似度矩阵
    item_similarity_content = cosine_similarity(item_features_matrix)
    
    # 获取用户的评分记录
    user_id = database['users'].index(user_name)
    user_ratings = ratings_matrix[user_id]
    
    # 计算协同过滤的推荐得分
    cf_scores = item_similarity_cf.dot(user_ratings)
    
    # 计算基于内容的推荐得分
    content_scores = item_similarity_content.dot(user_ratings)
    
    # 混合得分 = alpha * 协同过滤得分 + (1 - alpha) * 基于内容的得分
    hybrid_scores = alpha * cf_scores + (1 - alpha) * content_scores
    
    # 对于用户已经评分的商品，得分设为 0，避免重复推荐
    hybrid_scores[user_ratings > 0] = 0
    
    # 返回得分最高的商品
    recommended_items = np.argsort(hybrid_scores)[::-1][:top_n]
    return [database['items'][i] for i in recommended_items]

# ===========================
# 测试推荐系统
# ===========================

# 协同过滤推荐
print(f"协同过滤推荐给 Alice 的商品: {collaborative_filtering_recommend('Alice', database)}")

# 基于内容推荐
print(f"基于内容推荐给 Alice 的商品: {content_based_recommend('Alice', database)}")

# 混合推荐
print(f"混合推荐给 Alice 的商品: {hybrid_recommend('Alice', database)}")
