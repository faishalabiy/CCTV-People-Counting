import cv2
import requests
import base64
import time
import datetime

# Fungsi untuk membaca daftar alamat IP kamera dari file konfigurasi
def read_camera_ips(file_path="camera_ip.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return []

# Fungsi untuk mengambil capture image dari kamera
def capture_image(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    
    # Pastikan kamera terbuka dengan benar
    if not cap.isOpened():
        print("Error: Gagal membuka kamera.")
        return None

    # Baca frame dari kamera
    ret, frame = cap.read()

    # Tutup kamera
    cap.release()

    if ret:
        return frame
    else:
        print("Error: Gagal membaca frame.")
        return None

# Fungsi untuk membuat file log
def create_log(message):
    log_filename = "image_upload_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_filename, "a") as log_file:
        log_file.write(f"{timestamp}: {message}\n")

# Fungsi untuk mengirim capture image ke server
def send_image_to_server(image, server_ip, server_port):
    # Konversi gambar ke format base64
    _, img_encoded = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(img_encoded.tobytes())

    # Tentukan URL server
    server_url = f"http://{server_ip}:{server_port}/upload"

    # Data yang akan dikirimkan ke server
    payload = {'image': img_base64}

    try:
        # Kirim permintaan POST ke server
        response = requests.post(server_url, data=payload)

        # Tampilkan respons dari server
        print("Server Response:", response.text)

        # Tambahkan log ke file
        create_log(f"Image sent to server ({server_ip}). Response: {response.text}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    camera_ips = read_camera_ips()

    if not camera_ips:
        print("Error: Tidak ada alamat IP kamera yang dibaca.")
    else:
        while True:
            for camera_ip in camera_ips:
                image = capture_image()

                if image is not None:
                    send_image_to_server(image, camera_ip, "port_server")

                time.sleep(5)
