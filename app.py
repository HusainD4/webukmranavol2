import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Variabel untuk menyimpan konten
home_content = "<div id='home'><h1>Selamat datang di halaman Home!</h1></div>"
pendaftaran_content = "<div id='pendaftaran'><h1>Informasi Pendaftaran</h1></div>"
tentang_kami_content = "<div id='tentang_kami'><h1>Tentang Kami</h1></div>"
css_content = "body { font-family: Arial, sans-serif; }"
js_content = "console.log('Hello World');"

# Path untuk file CSS dan JS
CSS_PATH = 'static/css/styleshome.css'
JS_PATH = 'static/js/scripthome.js'

# Direktori untuk menyimpan file CSS, JS, dan HTML yang diubah
STATIC_FOLDER = 'static'
CSS_FOLDER = os.path.join(STATIC_FOLDER, 'css')
JS_FOLDER = os.path.join(STATIC_FOLDER, 'js')
TEMPLATES_FOLDER = 'templates'

# Pengaturan upload file
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'upload/foto/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Folder to store uploaded photos
UPLOAD_FOLDER = 'static/upload/foto/'

# List of images
def get_images():
    return os.listdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Daftar foto untuk menampung data yang diupload
photos = []

# Pastikan folder yang dibutuhkan ada
os.makedirs(CSS_FOLDER, exist_ok=True)
os.makedirs(JS_FOLDER, exist_ok=True)
os.makedirs(TEMPLATES_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fungsi untuk mengecek ekstensi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    images = get_images()  # Get the list of image files
    return render_template('home.html', content=home_content, images=images)

@app.route('/pendaftaran')
def pendaftaran():
    return render_template('pendaftaran.html')

@app.route('/tentang_kami')
def tentang_kami():
    return render_template('tentang_kami.html', content=tentang_kami_content)

@app.route('/galeri_kami')
def galeri_kami():
    images = get_images()  # Get the list of image files
    return render_template('galeri_kami.html', photos=photos, images=images)

@app.route('/upload_foto', methods=['GET', 'POST'])
def upload_foto():
    if request.method == 'POST':
        file = request.files.get('file')
        caption = request.form.get('caption')
        creator = request.form.get('creator')
        year = request.form.get('year')

        # Validasi input
        if not file or not allowed_file(file.filename):
            flash('File tidak valid atau tidak ada file yang diunggah!')
            return redirect(request.url)

        if not caption or not creator or not year:
            flash('Semua field harus diisi!')
            return redirect(request.url)

        # Buat nama file unik
        unique_filename = f"{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Simpan file ke folder upload
        file.save(filepath)

        # Tambahkan data ke daftar foto dengan id unik
        photo_id = uuid.uuid4().hex  # Generate unique ID for the photo
        photos.append({
            'id': photo_id,            # Store the ID in the dictionary
            'nama': unique_filename,
            'caption': caption,
            'creator': creator,
            'tahun': year,
            'path': f'upload/foto/{unique_filename}'
        })

        flash('Foto berhasil diunggah!')
        return redirect(url_for('galeri_kami'))

    return render_template('upload_foto.html')

@app.route('/hapus_foto/<string:photo_id>', methods=['POST'])
def hapus_foto(photo_id):
    global photos

    # Find the photo to delete by its unique 'id'
    photo_to_delete = next((photo for photo in photos if photo['id'] == photo_id), None)

    if photo_to_delete:
        # Delete the photo from the list
        photos = [photo for photo in photos if photo['id'] != photo_id]

        # Also delete the photo file from the server
        photo_file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_to_delete['nama'])
        if os.path.exists(photo_file_path):
            os.remove(photo_file_path)

        flash('Foto berhasil dihapus!')
    else:
        flash('Foto tidak ditemukan!')

    return redirect(url_for('galeri_kami'))

def save_content_to_files():
    with open(os.path.join(TEMPLATES_FOLDER, 'home.html'), 'w') as f:
        f.write(home_content)
    with open(os.path.join(TEMPLATES_FOLDER, 'pendaftaran.html'), 'w') as f:
        f.write(pendaftaran_content)
    with open(os.path.join(TEMPLATES_FOLDER, 'tentang_kami.html'), 'w') as f:
        f.write(tentang_kami_content)

if __name__ == '__main__':
    app.run(debug=True)
