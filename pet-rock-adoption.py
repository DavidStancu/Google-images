import os
from flask import Flask, request, render_template, redirect, send_from_directory, url_for, flash, session
from PIL import Image, ImageOps

app = Flask(__name__, static_folder="static")
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['THUMBNAIL_FOLDER'] = os.path.join('static', 'thumbnails')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

ALLOWED_USERS = {
    "pebble": "pebble123",
}

def thumbnail(image_path, thumbnail_path, size=(200, 200)):
    print("Generating thumbnail for:", image_path)
    print("Thumbnail will be saved at:", thumbnail_path)
    try:
        with Image.open(image_path) as original_image:
            thumbnail = ImageOps.fit(original_image, size, Image.LANCZOS)
            thumbnail.save(thumbnail_path)
            print("Thumbnail generated successfully.")
            return True
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return False
    except Exception as e:
        print(f"Error generating thumbnail for {image_path}: {e}")
        return False

@app.route('/')
def home():
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    user_thumbnail_folder = os.path.join(app.config['THUMBNAIL_FOLDER'], username)

    if not os.path.exists(user_upload_folder):
        os.makedirs(user_upload_folder)
    if not os.path.exists(user_thumbnail_folder):
        os.makedirs(user_thumbnail_folder)

    categories = {}
    for category in os.listdir(user_upload_folder):
        category_folder = os.path.join(user_upload_folder, category)
        if os.path.isdir(category_folder):
            images = os.listdir(category_folder)
            thumbnails = [image for image in images if os.path.exists(os.path.join(user_thumbnail_folder, category, image))]
            if thumbnails:
                categories[category] = thumbnails

    if not categories:
        flash('You have not added any photos to your collection. Click "Upload".', 'info')

    return render_template('home.html', categories=categories, username=username)

@app.route('/about')
def about():
    return render_template('about.html', title="About Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already logged in!', 'info')
        return redirect(url_for('home'))
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in ALLOWED_USERS and ALLOWED_USERS[username] == password:
            session['username'] = username
            flash('You have successfully logged in!', 'success')
            return redirect(url_for("home"))
        else:
            error_msg = "Invalid username or password"
    return render_template("login.html", error_msg=error_msg)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    user_thumbnail_folder = os.path.join(app.config['THUMBNAIL_FOLDER'], username)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No image part', 'danger')
            return redirect(request.url)

        image = request.files['file']
        image_name = request.form.get('image_name', 'Unnamed')
        category = request.form.get('category', 'uncategorized')
        if image.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        category_folder = os.path.join(user_upload_folder, category)
        thumbnail_category_folder = os.path.join(user_thumbnail_folder, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        if not os.path.exists(thumbnail_category_folder):
            os.makedirs(thumbnail_category_folder)

        image_path = os.path.join(category_folder, image.filename)
        image.save(image_path)

        thumbnail_path = os.path.join(thumbnail_category_folder, image.filename)
        thumbnail(image_path, thumbnail_path)

        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('upload.html')

@app.route('/image/<username>/<category>/<filename>')
def image(username, category, filename):
    print(filename)
    if 'username' not in session:
        flash('You need to log in first!', 'warning') 
        return redirect(url_for('login')) 
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], username, category)
    return send_from_directory(user_upload_folder, filename)

@app.route('/delete_image/<category>/<filename>', methods=['POST'])
def delete_image(category, filename):
    print(filename)
    if 'username' not in session:
        flash('You need to log in first!', 'warning') 
        return redirect(url_for('login')) 

    username = session['username']
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], username, category)
    user_thumbnail_folder = os.path.join(app.config['THUMBNAIL_FOLDER'], username, category)

    try:
        image_path = os.path.join(user_upload_folder, filename)
        thumbnail_path = os.path.join(user_thumbnail_folder, filename)
        os.remove(image_path)
        os.remove(thumbnail_path)
        flash('Image deleted successfully!', 'success') 
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error deleting image: {e}', 'danger')
        return redirect(url_for('home'))

@app.errorhandler(404)
def error404(code):
    return "HTTP Error 404 - Page Not Found"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
