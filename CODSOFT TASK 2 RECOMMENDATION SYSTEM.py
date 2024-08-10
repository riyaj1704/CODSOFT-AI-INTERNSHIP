import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample data
user_ratings = {
    'User1': {'Matrix': 5, 'Titanic': 3, 'Inception': 4},
    'User2': {'Matrix': 3, 'Titanic': 4, 'Inception': 2, 'Avatar': 5},
    'User3': {'Matrix': 4, 'Titanic': 5, 'Avatar': 3},
    'User4': {'Titanic': 5, 'Avatar': 4},
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(user_ratings).T.fillna(0)

# Calculate similarity matrix
similarity_matrix = cosine_similarity(df)
similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

def get_recommendations(user, num_recommendations=2):
    # Find similar users
    similar_users = similarity_df[user].sort_values(ascending=False).index[1:]
    
    # Aggregate ratings of similar users
    user_ratings_weighted_sum = np.zeros(df.shape[1])
    similarity_sum = 0
    for similar_user in similar_users:
        similarity = similarity_df.loc[user, similar_user]
        similarity_sum += similarity
        user_ratings_weighted_sum += similarity * df.loc[similar_user].values

    # Normalize by the sum of similarities
    if similarity_sum == 0:
        return []

    user_ratings_normalized = user_ratings_weighted_sum / similarity_sum
    
    # Convert to a DataFrame
    user_ratings_normalized_df = pd.DataFrame(user_ratings_normalized, index=df.columns, columns=['score'])
    
    # Filter out movies the user has already rated
    rated_movies = df.loc[user] > 0
    recommendations = user_ratings_normalized_df[~rated_movies].sort_values(by='score', ascending=False)
    
    # Get the top N recommendations
    return recommendations.head(num_recommendations).index.tolist()

# Test the recommendation system
user = 'User1'
recommendations = get_recommendations(user, num_recommendations=2)
print(f'Recommendations for {user}: {recommendations}')
