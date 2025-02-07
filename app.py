import os
import time
import threading
from datetime import timedelta, datetime
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'replace_with_a_secret_key'  # Needed for flash messages

# Function to delete a file after a delay (in seconds)
def delete_file_later(filepath, delay_seconds):
    def delete():
        # Wait for the specified delay
        time.sleep(delay_seconds)
        # If the file still exists, remove it
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deleted {filepath}")
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
    # Run the deletion in a daemon thread
    t = threading.Thread(target=delete)
    t.daemon = True
    t.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash("No file part in the request!")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)
        
        # Save the file
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # Get the expiration time (in seconds) from the form.
        # The dropdown values are set directly in seconds:
        # 300 = 5 minutes, 600 = 10 minutes, 3600 = 1 hour, 36000 = 10 hours, 86400 = 24 hours.
        try:
            delay_seconds = int(request.form.get('expiration', 300))
        except ValueError:
            delay_seconds = 300

        # Schedule the file for deletion
        delete_file_later(save_path, delay_seconds)
        flash("File uploaded successfully!")
        return redirect(url_for('index'))

    # For GET requests, list all files currently in the upload folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/files/<filename>')
def download_file(filename):
    # Serve the file as an attachment (download)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # Host on all interfaces so that devices on your home Wi-Fi can connect
    app.run(host="0.0.0.0", port=5000, debug=False)
