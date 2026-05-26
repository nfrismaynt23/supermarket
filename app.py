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

# --- CUSTOM CSS: PREMIUM MINIMALIST & CLEAN ---
custom_css = """
<style>
    .stApp {
        background-color: #0b0f17 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #06090e !important;
        border-right: 1px solid #1e293b !important;
    }
    h1, h2, h3, h4, p, span, label, li, div {
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    [data-testid="stWidgetLabel"] p, .st-dc, .st-da, .st-db {
        color: #94a3b8 !important;
    }
    .clean-box {
        background: #111827 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
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
        "Tissu Wajah 200 sheets": 9000
    }

antrean = st.session_state.antrean_kasir

# ==========================================
# HALAMAN 1: LOGIN (BERSIH & FORMAL)
# ==========================================
if not st.session_state.is_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:60px; margin-bottom:20px;">', unsafe_allow_html=True)
        logo_url = "https://global.ac.id/wp-content/uploads/2021/01/logo-global-80.png"
        st.image(logo_url, width=130)
        st.markdown('<h1 style="font-size: 28px; font-weight: 600; letter-spacing: 1px; margin-top:15px;">FreshMart Express</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #64748b; font-size: 13px;">Sistem Informasi Manajemen Antrean Kasir</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username / NIK Pegawai:")
        password = st.text_input("Password:", type="password")
        
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Kredensial yang Anda masukkan salah.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: DASHBOARD UTAMA
# ==========================================
else:
    st.sidebar.markdown("<h3 style='letter-spacing: 1px; font-weight:600; margin-bottom:0;'>FreshMart Express</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#64748b; font-size:12px; margin-top:0;'>Otoritas Kasir: Aktif</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Navigasi:",
        [
            "Beranda Utama", 
            "Daftar Produk Toko",
            "Monitor Antrean", 
            "Tambah Pelanggan Baru", 
            "Proses Pembayaran (Checkout)", 
            "Riwayat Jurnal Transaksi"
        ]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Keluar Sistem", type="secondary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()

    # MENU 1: BERANDA UTAMA (SUDAH DIPERBAIKi JADI JAUH LEBIH INTERAKTIF)
    if menu == "Beranda Utama":
        st.markdown('<h1 style="margin-bottom:0px;">Statistik Toko & Kasir</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; margin-bottom:25px;">Ringkasan aktivitas operasional retail secara real-time</p>', unsafe_allow_html=True)
        
        # Hitung jumlah antrean saat ini
        panjang_antrean = 0
        curr = antrean.head
        while curr:
            panjang_antrean += 1
            curr = curr.next
            
        # Layout Ringkasan Kartu Metrik (3 Kolom Sejajar)
        col_m1, col_m2, col_m3 = st.columns(3
