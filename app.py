import streamlit as st

# ==========================================
# KELAS NODE PELANGGAN & ANTRIAN (QUEUE)
# ==========================================
class PelangganNode:
    def __init__(self, nama, list_belanjaan, total_harga):
        self.nama = nama
        self.list_belanjaan = list_belanjaan  
        self.total_harga = total_harga        
        self.next = None

class QueueSupermarket:
    def __init__(self):
        self.head = None
        self.tail = None
        self.total_pelanggan_dilayani = 0

    def is_empty(self):
        return self.head is None

    def tambah_pelanggan(self, nama, list_belanjaan, total_harga):
        baru = PelangganNode(nama, list_belanjaan, total_harga)
        if self.is_empty():
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru

    def layani_pelanggan(self):
        if self.is_empty():
            return None
        pelanggan_dilayani = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.total_pelanggan_dilayani += 1
        return pelanggan_dilayani

    def dapatkan_antrean_string(self):
        if self.is_empty():
            return "Antrean Kosong"
        hasil = ""
        sekarang = self.head
        nomor = 1
        while sekarang:
            jumlah_item = len(sekarang.list_belanjaan)
            hasil += f"[{nomor}] {sekarang.nama} ({jumlah_item} Item Barang)\n"
            sekarang = sekarang.next
            nomor += 1
        return hasil

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="FreshMart Express", layout="wide")

# --- CUSTOM CSS: GRADASI BIRU CERAH & SCOPED TEXT (ANTI-TABRAKAN) ---
custom_css = """
<style>
    /* Latar Belakang Utama Aplikasi: Gradasi Biru Cerah Lembut */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%) !important;
    }
    
    /* Navigasi Samping (Sidebar) dengan Kontras Biru Lembut */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Judul Kustom Utama */
    .main-title {
        color: #1e3a8a !important;
        font-weight: 700 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    
    /* Kotak Konten Kustom (Clean Box) Berwarna Putih Bersih dengan Efek Shadow */
    .clean-box {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-left: 6px solid #0284c7 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* Pewarnaan Teks Khusus di Dalam Clean Box Saja */
    .clean-box p, .clean-box h4, .clean-box span {
        color: #334155 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    
    /* Memperbaiki Kotak Text Area agar Kontras di Background Cerah */
    textarea {
        color: #0f172a !important;
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INISIALISASI DATA DI SESSION STATE ---
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []

# MASTER DATABASE: 20 PRODUK SUPERMARKET
if 'database_produk' not in st.session_state:
    st.session_state.database_produk = {
        "Minyak Goreng 2L": 36000,
        "Susu UHT Full Cream 1L": 18500,
        "Mie Instan Goreng": 3500,
        "Beras Premium 5kg": 75000,
        "Gula Pasir 1kg": 17000,
        "Teh Celup Isi 25": 6000,
        "Kopi Bubuk 100g": 12000,
        "Roti Tawar Kupas": 15000,
        "Mentega Serbaguna": 8500,
        "Kecap Manis Bango": 24000,
        "Saus Sambal Botol": 14500,
        "Sabun Mandi Cair": 22000,
        "Shampoo Anti Dandruff": 28000,
        "Pasta Gigi Herbal": 12500,
        "Deterjen Bubuk 800g": 19500,
        "Cairan Pencuci Piring": 10500,
        "Air Mineral 600ml": 3500,
        "Keripik Kentang Snack": 11000,
        "Cokelat Batang Premium": 16000,
        "Tisu Wajah 200 sheets": 9000
    }

# Baris di bawah ini dipastikan sudah lengkap tanpa terputus:
antrean = st.session_state.antrean_kasir

# ==========================================
# HALAMAN 1: LOGIN (MENGGUNAKAN LOGO KAMPUS)
# ==========================================
if not st.session_state.is_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:60px; margin-bottom:20px;">', unsafe_allow_html=True)
        logo_url = "https://global.ac.id/wp-content/uploads/2021/01/logo-global-80.png"
        st.image(logo_url, width=130)
        st.markdown('<h1 class="main-title" style="font-size: 28px; letter-spacing: 1px; margin-top:15px;">FreshMart Express</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #475569; font-size: 13px;">Sistem Informasi Manajemen Antrean Kasir</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username / NIK Pegawai:")
        password = st.text_input("Password:", type="password")
        
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        if st.button("Masuk ke Sistem", type="primary", use_container_
                     
