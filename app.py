from flask import Flask, render_template, request, session, jsonify, url_for
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

keyword_list = []

# Global list to hold all uploaded articles
articles = []

@app.route('/upload', methods=['POST'])
def upload_article():
    """
    Receive an article (title, content, image, and keywords) from the local machine and store it in a global list.
    """
    try:
        title = request.form['title']
        content = request.form['content']
        image = request.files.get('image')
        keywords = request.form['keywords']

        # Store the article data in the global list
        article = {
            'title': title,
            'content': content,
            'image': image.read() if image else None,
            'image_filename': image.filename if image else None,
            'keywords': keywords
        }
        articles.append(article)

        return jsonify({"message": "Article received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Server-side storage of chat messages
chat_messages = []

# Home route to render the HTML page
@app.route('/')
def home():
    # Assign unique user ID for each session
    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'
    return render_template('index.html', user_id=session['user_id']) 

# Home route to render the HTML page
@app.route('/article')
def article():
    # Assign unique user ID for each session
    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'
    return render_template('article.html')



# routes to the search page
@app.route('/search')
def search():
    # Assign unique user ID for each session
    featured_articles = [
        {
            'title': article['title'],
            'content': article['content'],
            'image_url': url_for('serve_image', index=i) if article['image'] else None,
            'keywords': article['keywords']
        }
        for i, article in enumerate(articles)
    ]

    for article in articles:
        keywords = article['keywords'].split('|')
        print(keywords)
        for keyword in keywords:
            keyword = keyword.strip()
            if not keyword in keyword_list:
                keyword_list.append(keyword)

    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'
    return render_template('search.html', featured_articles = featured_articles, keywords = keyword_list)

@app.route('/image/<int:index>')
def serve_image(index):
    """
    Serve the image associated with the article at the given index.
    """
    if 0 <= index < len(articles) and articles[index]['image']:
        return articles[index]['image'], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "No image available", 404


# API to get the latest chat messages
@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(chat_messages)

@app.route('/smart_search')
def smart_search():
    return render_template('smart_search.html')

# API to send a new message
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    user_id = session.get('user_id', 'Anonymous')  # Get user ID from session
    if user_message:
        message_data = {
            'user': user_id,
            'message': user_message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        chat_messages.append(message_data)
    return '', 204  # Return success but no content


if __name__ == '__main__':
    app.run(debug=True)