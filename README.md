Local File Share
A simple Flask-based file-sharing web app that allows users connected to the same Wi-Fi network to upload and download files. Users can set an expiration time for their files, after which they are automatically deleted.

🚀 Features
✅ Upload and download any file (images, PDFs, ZIPs, text files, etc.).
✅ Files are accessible to all devices on the same Wi-Fi network.
✅ Choose how long a file remains available (5 min, 10 min, 1 hour, 10 hours, 24 hours).
✅ Clean and responsive UI for both mobile and desktop.

📦 Installation
Clone the repository

git clone https://github.com/your-username/local-file-share.git
cd local-file-share
Install dependencies

pip install -r requirements.txt
Run the application

python app.py
Access the web app

Open a browser and go to:
http://localhost:5000
Or, to allow access from other devices on the same Wi-Fi, find your local IP and replace localhost with it.

🔧 Configuration
Files are stored temporarily in the uploads/ folder.
Expired files are automatically deleted based on the selected time.
🛠 Future Improvements
Add password-protected uploads.
Implement QR code links for easy file sharing.
Support for multiple file uploads at once.
