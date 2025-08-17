from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
app.secret_key = 'your_secret_key'  


DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'marketing_sample_for_walmart_com-walmart_com_product_review__20200701_20201231__5k_data (1).tsv')
df = pd.read_csv(DATA_PATH, sep='\t')

# Preprocess columns (as in notebook)

df.fillna({
    'Product Rating': 0,
    'Product Reviews Count': 0,
    'Product Category': '',
    'Product Brand': '',
    'Product Description': '',
    'Product Tags': ''
}, inplace=True)

df['Uniq Id'] = df['Uniq Id'].astype(str)
df['Product Id'] = df['Product Id'].astype(str)

# Rename columns for easier access
df.rename(columns={
    'Uniq Id': 'ID',
    'Product Id': 'ProdID',
    'Product Rating': 'Rating',
    'Product Reviews Count': 'ReviewCount',
    'Product Category': 'Category',
    'Product Brand': 'Brand',
    'Product Name': 'Name',
    'Product Image Url': 'ImageURL',
    'Product Description': 'Description',
    'Product Tags': 'Tags'
}, inplace=True)

# --- Rating-based Recommendation (Trending Products) ---
def get_top_rated_products(n=5):
    avg_rating = df.groupby(['Name', 'ReviewCount', 'Brand', 'ImageURL'])['Rating'].mean().reset_index()
    top_rated = avg_rating.sort_values(by='Rating', ascending=False).head(n)
    return top_rated

# --- Content-based Recommendation ---
def get_content_based_recommendations(item_name, top_n=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Tags'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    if item_name not in df['Name'].values:
        return pd.DataFrame()
    idx = df[df['Name'] == item_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return df.iloc[top_indices][['Name', 'Brand', 'ImageURL', 'Rating']]

# --- User-based Recommendation (Simple Demo) ---
def get_user_based_recommendations(user_id, top_n=5):
    # For demo: recommend products highly rated by users with similar tastes
    user_ratings = df[df['ID'] == str(user_id)]
    if user_ratings.empty:
        return get_top_rated_products(top_n)
    liked = user_ratings[user_ratings['Rating'] >= 4]['ProdID'].tolist()
    similar_users = df[df['ProdID'].isin(liked) & (df['ID'] != str(user_id))]
    recs = similar_users.groupby('ProdID').agg({'Rating':'mean'}).sort_values('Rating', ascending=False).head(top_n)
    return df[df['ProdID'].isin(recs.index)][['Name', 'Brand', 'ImageURL', 'Rating']].drop_duplicates()

# --- Hybrid Recommendation ---
def get_hybrid_recommendations(user_id, item_name, top_n=5):
    # Combine content and user-based recommendations
    content_recs = get_content_based_recommendations(item_name, top_n=top_n*2)
    user_recs = get_user_based_recommendations(user_id, top_n=top_n*2)
    hybrid = pd.concat([content_recs, user_recs]).drop_duplicates().head(top_n)
    return hybrid

@app.route('/', methods=['GET', 'POST'])
def home():
    # Remove any POST search logic from GET requests
    if request.method == 'POST':
        search_query = request.form.get('search')
        if search_query:
            match = df[df['Name'].str.contains(search_query, case=False, na=False)]
            if not match.empty:
                prod_id = match.iloc[0]['ProdID']
                return redirect(url_for('product_search', prod_id=prod_id))
            else:
                flash(f"No product found for '{search_query}'", "error")
        # After handling POST, return/redirect to avoid falling through to GET logic

    rating_recs = get_top_rated_products(10)
    rec_type = "Rating-based Recommendations (Trending Products)"
    # Only pass variables needed for home.html
    return render_template(
        'home.html',
        rating_recs=rating_recs,
        rec_type=rec_type
    )

@app.route('/product_search/<prod_id>')
def product_search(prod_id):
    product = df[df['ProdID'] == str(prod_id)].iloc[0].to_dict()
    content_recs = get_content_based_recommendations(product['Name'], top_n=10)
    rec_type = f"Top 10 Content-based Recommendations for '{product['Name']}'"
    return render_template(
        'product_search.html',
        product=product,
        content_recs=content_recs,
        rec_type=rec_type
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user_id'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user_recs = get_user_based_recommendations(user_id, top_n=5)
    hybrid_recs = get_hybrid_recommendations(user_id, user_recs.iloc[0]['Name'] if not user_recs.empty else '', top_n=5)
    return render_template(
        'dashboard.html',
        user_id=user_id,
        user_recs=user_recs,
        hybrid_recs=hybrid_recs
    )

@app.route('/product/<prod_id>')
def product_detail(prod_id):
    product = df[df['ProdID'] == str(prod_id)].iloc[0]
    content_recs = get_content_based_recommendations(product['Name'])
    return render_template('product.html', product=product, recommendations=content_recs)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        item_name = request.form.get('item_name')
        rec_type = request.form.get('rec_type')
        if rec_type == 'rating':
            recs = get_top_rated_products()
        elif rec_type == 'content':
            recs = get_content_based_recommendations(item_name)
        elif rec_type == 'user':
            recs = get_user_based_recommendations(user_id)
        elif rec_type == 'hybrid':
            recs = get_hybrid_recommendations(user_id, item_name)
        else:
            recs = pd.DataFrame()
        return render_template('recommend.html', recommendations=recs)
    return render_template('recommend.html', recommendations=None)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
