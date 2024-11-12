import os
import re
import requests
import random
from flask import Flask, request, jsonify, render_template, session, send_from_directory, url_for
#from flask import Flask, render_template, url_for, send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


articles = []
keyword_list = ['test1', 'test2', 'test3']

# Directory to store articles locally
ARTICLES_DIR = "./articles/newList"
os.makedirs(ARTICLES_DIR, exist_ok=True)

def sanitize_title(title):
    """
    Sanitize the title to remove any irregular symbols and truncate it at the first occurrence of " _ ".
    - Replace spaces and other whitespace with hyphens.
    - Remove any non-alphanumeric characters except hyphens and underscores.
    - Convert to lowercase for consistency.
    - Truncate the title at the first occurrence of " _ " and remove everything after it.
    """
    title = title.strip()

    # Remove everything after the first occurrence of " _ "
    title = title.split(" _ ")[0]

    # Replace spaces and other whitespace characters with hyphens
    title = re.sub(r'\s+', ' ', title)

    # Remove any non-alphanumeric characters (excluding hyphens and underscores)
    title = re.sub(r'[^a-zA-Z0-9\-_]', ' ', title)

    # Optionally, convert to lowercase (useful for URLs)
    #title = title.lower()

    return title

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

def send_article_to_server(title, content, image_path, keywords):
    """
    Send the article's title, content, and image to the remote Flask server.
    """
    url = 'http://127.0.0.1:5000/upload'

    files = {
        'title': (None, title),
        'content': (None, content),
        'keywords': (None, keywords)
    }

    if image_path and os.path.exists(image_path):
        files['image'] = open(image_path, 'rb')

    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print(f"Successfully uploaded article: {title}")
        else:
            print(f"Failed to upload article: {response.status_code}")
    except Exception as e:
        print(f"Error uploading article '{title}': {e}")
    finally:
        if 'image' in files:
            files['image'].close()
    print(f"Sending {title} with content of length {len(content)} and image {image_path}")

def load_and_send_articles():
    """
    Load articles from the local directory and send them to the remote server.
    """

    print(f"Loading articles from {ARTICLES_DIR}...")  # Debug

    for folder_name in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if os.path.isdir(folder_path):
            try:
                files_in_folder = os.listdir(folder_path)
                
                article_file = 'title.txt'
                content_file = 'content.txt'
                image_file = 'image.jpg'
                keyword_file = 'keywords.txt'

                article_path = os.path.join(folder_path, article_file)
                content_path = os.path.join(folder_path, content_file)
                image_path = os.path.join(folder_path, image_file)
                keyword_path = os.path.join(folder_path, keyword_file)

               # Check if all expected files exist
                if not (os.path.isfile(article_path) and os.path.isfile(image_path)):
                    print(f"Missing files in folder: {folder_name}")
                    continue  # Skip to the next folder if files are missing

                print(f"Folder: {folder_name}")
                print(f"Article files: {article_file}")
                print(f"Content files: {content_file}")
                print(f"Image files: {image_file}")
                print(f"Keywords: {keyword_file}")
  
                with open(article_path, 'r', encoding='utf-8') as file:
                    title = sanitize_title(file.read().strip())
                
                with open(content_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()

                with open(keyword_path, 'r', encoding='utf-8') as file:
                    keywords = file.read().strip()

                print(f"Sending article: {title}")  # Debug

                # Send the article to the remote server
                send_article_to_server(title, content, image_path, keywords)
                #print("article", articles)

                '''articles.append({
                'title': title,
                'content': content,
                'image': image_path if image_path and os.path.exists(image_path) else None
            })'''

            except Exception as e:
                print(f"Error loading article in folder '{folder_name}': {e}")
    print("Finished loading and sending all articles!")  # Debug

# routes to the search page
@app.route('/search')
def search():
    if not articles:
        load_and_send_articles()

    # Assign unique user ID for each session
    featured_articles = [
        {
            'title': article['title'],
            'content': article['content'],
            'image_url': url_for('serve_image', index=i) if article['image'] else None
        }

        for i, article in enumerate(articles)
    ]

    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'
    print(featured_articles, "printeddddd")
    return render_template('search.html', featured_articles = featured_articles, keywords = keyword_list)


@app.route('/')
def home():
    """
    Load and display articles stored locally.
    """
    # load_and_send_articles()  # Load and send articles when the script starts

    
    '''for folder_name in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if os.path.isdir(folder_path):
            title_path = os.path.join(folder_path, 'title.txt')
            content_path = os.path.join(folder_path, 'content.txt')
            image_path = os.path.join(folder_path, 'image.jpg')

            with open(title_path, 'r', encoding='utf-8') as file:
                title = file.read().strip()

            with open(content_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            image_url = url_for('serve_image', folder_name=folder_name, image_name='image.jpg') if os.path.exists(image_path) else url_for('static', filename='default.jpg')

            articles.append({
                'title': title,
                'content': content,
                'image_url': image_url,
            })'''
    featured_articles = [
        {
            'title': article['title'],
            'content': article['content'],
            'image_url': url_for('serve_image', index=i) if article['image'] else None
        }

        for i, article in enumerate(articles)
    ]
    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'
    return render_template('index.html', featured_articles=featured_articles, user_id=session['user_id'])

'''@app.route('/articles/<folder_name>/<image_name>')
def serve_image(folder_name, image_name):
    """
    Serve images from the local articles directory.
    """
    image_dir = os.path.join(ARTICLES_DIR, folder_name)
    return send_from_directory(image_dir, image_name)'''

@app.route('/image/<int:index>')
def serve_image(index):
    """
    Serve the image associated with the article at the given index.
    """
    if 0 <= index < len(articles) and articles[index]['image']:
        return articles[index]['image'], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "No image available", 404

@app.route('/article', methods=['GET'])
def article():
    """
    Search for articles based on the 'q' query parameter (e.g. ?q=keyword).
    """
    query = request.args.get('q').lower()
    filtered_articles = [
        {
            'title': article['title'],
            'content': article['content'],
            'image_url': url_for('serve_image', index=i) if article['image'] else None
        }

        for i, article in enumerate(articles) if query in article['keywords'].lower()
    ]

    keyword_list.append(query)

    if 'user_id' not in session:
        session['user_id'] = f'User{random.randint(1000, 9999)}'

    return render_template('search.html', featured_articles=filtered_articles, keywords=keyword_list)


if __name__ == '__main__':
    
    app.run(debug=True)
    
    