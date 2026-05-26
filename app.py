import streamlit as st
import time

# ==========================================
# KELAS NODE PELANGGAN & ANTRIAN (QUEUE)
# ==========================================
class PelangganNode:
    def __init__(self, nama, jumlah_barang):
        self.nama = nama
        self.jumlah_barang = jumlah_barang
        self.next = None

class QueueSupermarket:
    def __init__(self):
        self.head = None
        self.tail = None
        self.total_pelanggan_dilayani = 0

    def is_empty(self):
        return self.head is None

    def tambah_pelanggan(self, nama, jumlah_barang):
        baru = PelangganNode(nama, jumlah_barang)
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
            return "--- Antrean Kosong / Kasir Senggang ---"
        hasil = ""
        sekarang = self.head
        nomor = 1
        while sekarang:
            hasil += f"[{nomor}] {sekarang.nama} ({sekarang.jumlah_barang} Barang)\n"
            sekarang = sekarang.next
            nomor += 1
        return hasil

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="Checkout Supermarket", page_icon="🛒", layout="wide")

# --- CUSTOM CSS CLEAN & PROFESSIONAL THEME ---
# Memaksa warna background dan teks agar konsisten & tajam (Anti Gagal Dark Mode)
custom_css = """
<style>
    /* Background utama aplikasi dibuat abu-abu sangat muda bersih */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Memaksa semua teks reguler berwarna gelap tajam agar terbaca */
    p, span, label, th, td, h1, h2, h3, h4 {
        color: #0F172A !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Judul Premium */
    .app-title {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important; /* Warna Biru Navy Profesional */
        margin-bottom: 2px !important;
    }
    
    .app-subtitle {
        font-size: 18px !important;
        font-weight: 400 !important;
        color: #475569 !important;
        margin-bottom: 30px !important;
    }

    /* Kotak Informasi Berwarna Solid & Kontras Tinggi */
    .info-box {
        background-color: #FFFFFF !important;
        border-left: 5px solid #2563EB !important; /* Aksen Biru */
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 25px !important;
    }
    
    /* Kartu Statistik Angka */
    .stat-card-red {
        background-color: #FEF2F2 !important; /* Merah Muda Halus */
        border: 1px solid #FCA5A5 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }
    
    .stat-card-green {
        background-color: #F0FDF4 !important; /* Hijau Muda Halus */
        border: 1px solid #86EFAC !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Inisialisasi session state
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()

antrean = st.session_state.antrean_kasir

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🏪 Navigasi Menu")
st.sidebar.write("Silakan pilih menu:")

menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "👥 Lihat Antrean", "➕ Tambah Pelanggan", "🧾 Proses Checkout", "ℹ️ Tentang Aplikasi"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🚨 Reset Sistem Kasir", type="secondary"):
    st.session_state.antrean_kasir = QueueSupermarket()
    st.success("Sistem berhasil direset!")
    time.sleep(1)
    st.rerun()

# ==========================================
# LOGIKA HALAMAN
# ==========================================

# MENU 1: BERANDA
if menu == "🏠 Beranda":
    st.markdown('<h1 class="app-title">🛒 Selamat Datang di Simulasi Antrean Supermarket</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Sistem Manajemen Antrean Kasir Berbasis Struktur Data Queue (FIFO)</p>', unsafe_allow_html=True)
    
    # Box Informasi Utama
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top:0; color:#1E3A8A !important; font-weight:700;">💡 Cara Kerja Sistem (Struktur Data Queue)</h4>
        <p style="margin:0; font-size:15px; line-height:1.6;">
            Aplikasi ini mensimulasikan alur pelayanan kasir di sebuah market secara riil. 
            Menggunakan metode <b>First In, First Out (FIFO)</b>, pelanggan yang pertama kali mengantre 
            akan diprioritaskan untuk dilayani terlebih dahulu sebelum pelanggan yang datang setelahnya.
        </p>
    </div>
