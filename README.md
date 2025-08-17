# Demo E-Commerce Product Recommendation System

A Flask-based demo e-commerce site with multiple recommendation algorithms using a Walmart product review dataset.

---

## Demo




https://github.com/user-attachments/assets/f83ac153-1ffc-48c0-b88d-bedb5c4abf9f




## Technologies Used

- **Python 3**
- **Flask** (Web framework)
- **pandas** (Data manipulation)
- **scikit-learn** (Machine learning, text vectorization, similarity)
- **HTML/CSS (Jinja2 templates)** (Frontend)
- **Bootstrap-inspired custom CSS** (UI/UX)
- **Session-based authentication** (Simple username login)

---

## Recommendation Methods

### 1. **Rating-based (Trending) Recommendation**
- **How it works:**  
  Calculates the average rating for each product and recommends the top-rated products across all users.
- **Use case:**  
  Shows what is trending or highly rated by everyone.

### 2. **Content-based Recommendation**
- **How it works:**  
  Uses product tags and descriptions. Text data is vectorized using TF-IDF, and cosine similarity is computed between products. For a given product, the most similar products are recommended.
- **Use case:**  
  Shows products similar in content to the one being viewed or searched.

### 3. **User-based Recommendation**
- **How it works:**  
  For a given user, finds products highly rated by users with similar tastes (i.e., who liked the same products). Recommends items those similar users liked.
- **Use case:**  
  Personalized recommendations based on user behavior.

### 4. **Hybrid Recommendation**
- **How it works:**  
  Combines content-based and user-based recommendations, merging both lists and removing duplicates.
- **Use case:**  
  Offers a balance between personal taste and product similarity.

---

## Project Structure

```
product_recomendation/
│
├── Data/
│   └── marketing_sample_for_walmart_com-walmart_com_product_review__20200701_20201231__5k_data (1).tsv
│
├── project/
│   └── app.py
│
├── templates/
│   ├── home.html
│   ├── product.html
│   ├── product_search.html
│   ├── dashboard.html
│   ├── login.html
│   └── recommend.html
│
├── static/
│   └── style.css
│
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone or Download the Repository

Place all files as shown above.

### 2. Install Python Dependencies

Create a virtual environment (recommended):

```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On Mac/Linux:
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, create one with:

```bash
pip freeze > requirements.txt
```

Or use:

```
Flask
pandas
scikit-learn
```

### 3. Data File

Ensure the data file is present at:

```
Data/marketing_sample_for_walmart_com-walmart_com_product_review__20200701_20201231__5k_data (1).tsv
```

If you move it, update the `DATA_PATH` in `project/app.py`.

---

## Running the App

From the `project` directory, run:

```bash
python app.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## Usage Guide

- **Home:**  
  - See trending products (rating-based).
  - Use the search bar for content-based recommendations.

- **Login:**  
  - Click "Login", enter any username.

- **Dashboard:**  
  - See user-based and hybrid recommendations.

- **Product Page:**  
  - Click a product to see details and similar products.

- **General Recommendations:**  
  - Visit `/recommend` to try all recommendation types.

---

## Customization

- **Styling:**  
  Edit `static/style.css` for UI changes.

- **Templates:**  
  Edit HTML files in `templates/` for layout/content.

- **Recommendation Logic:**  
  See `project/app.py` for all logic.

---

## Troubleshooting

- **FileNotFoundError:**  
  Ensure your data file path matches `DATA_PATH` in `app.py`.

- **Jinja2 Template Errors:**  
  Check for unclosed `{% for %}` or `{% if %}` blocks in your templates.

- **Port in Use:**  
  If port 5000 is busy, run with `python app.py --port 5001` (after editing `app.py`).

---

## License

For demo/educational use only.

---

## Author

- Built with ❤️ using Flask, pandas, and scikit-learn.
