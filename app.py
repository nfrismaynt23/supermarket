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

# --- CUSTOM CSS UNTUK BACKGROUND & FONT KEREN ---
custom_css = """
<style>
    /* Mengganti background utama dengan gambar supermarket blur transparan */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url('https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Mengubah font global agar estetik */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        color: #1E293B !important;
    }
    
    /* Styling Judul Utama */
    .main-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }
    
    /* Styling Subjudul */
    .sub-title {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        margin-bottom: 25px;
    }

    /* Membuat kartu/kotak informasi jadi efek Glassmorphism transparan mentereng */
    .custom-card {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05) !important;
        margin-bottom: 20px;
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
    st.markdown('<p class="main-title">🛒 Selamat Datang di Simulasi Antrean Supermarket</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Sistem Manajemen Antrean Kasir Berbasis Struktur Data Queue (FIFO)</p>', unsafe_allow_html=True)
    
    # Bungkus deskripsi ke dalam Custom Card (Efek Glassmorphism)
    st.markdown("""
    <div class="custom-card">
        <h3>💡 Informasi Sistem</h3>
        <p>Aplikasi ini dirancang untuk mensimulasikan bagaimana sebuah antrean di kasir supermarket berjalan secara riil. 
        Dengan menggunakan prinsip utama <b>First In, First Out (FIFO)</b>, pelanggan yang masuk antrean pertama kali 
        akan menjadi yang pertama diproses pembayarannya oleh kasir.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### 📊 Status Kasir Saat Ini")
    
    # Hitung antrean
    panjang = 0
    curr = antrean.head
    while curr:
        panjang += 1
        curr = curr.next
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <p style="margin:0; font-size:16px; color:#64748B;">Pelanggan Menunggu</p>
            <p style="margin:0; font-size:36px; font-weight:700; color:#EF4444;">{panjang} Orang</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <p style="margin:0; font-size:16px; color:#64748B;">Total Sukses Dilayani</p>
            <p style="margin:0; font-size:36px; font-weight:700; color:#10B981;">{antrean.total_pelanggan_dilayani} Orang</p>
        </div>
        """, unsafe_allow_html=True)

# MENU 2: LIHAT ANTREAN
elif menu == "👥 Lihat Antrean":
    st.markdown('<p class="main-title">👥 Kondisi Antrean Kasir Saat Ini</p>', unsafe_allow_html=True)
    
    panjang = 0
    curr = antrean.head
    while curr:
        panjang += 1
        curr = curr.next

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Jumlah Antrean Sekarang", value=f"{panjang} Orang")
    with col2:
        st.metric(label="Total Pelanggan Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang")
    
    st.write("---")
    antrean_teks = antrean.dapatkan_antrean_string()
    st.text_area("Daftar Antrean (Urutan teratas adalah yang terdepan):", value=antrean_teks, height=250, disabled=True)

# MENU 3: TAMBAH PELANGGAN
elif menu == "➕ Tambah Pelanggan":
    st.markdown('<p class="main-title">➕ Masukkan Pelanggan Baru</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    with st.form("form_pelanggan", clear_on_submit=True):
        nama_pelanggan = st.text_input("Nama Pelanggan:")
        jumlah_item = st.number_input("Jumlah Barang Belanjaan:", min_value=1, max_value=100, value=5)
        submit_button = st.form_submit_button("Masuk Antrean", type="primary")
        
        if submit_button:
            if nama_pelanggan.strip():
                antrean.tambah_pelanggan(nama_pelanggan, jumlah_item)
                st.success(f"🛒 '{nama_pelanggan}' ({jumlah_item} barang) berhasil masuk ke antrean!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Harap masukkan nama pelanggan terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

# MENU 4: PROSES CHECKOUT
elif menu == "🧾 Proses Checkout":
    st.markdown('<p class="main-title">🧾 Meja Kasir (Proses Pelayanan)</p>', unsafe_allow_html=True)
    
    if antrean.is_empty():
        st.info("🎉 Semua antrean sudah selesai diproses. Kasir sedang senggang!")
    else:
        pelanggan_depan = antrean.head
        st.warning(f"Pelanggan berikutnya yang harus dilayani: **{pelanggan_depan.nama}** ({pelanggan_depan.jumlah_barang} barang).")
        
        if st.button("Proses & Selesaikan Pembayaran", type="primary"):
            dilayani = antrean.layani_pelanggan()
            if dilayani:
                st.success(f"✅ Selesai! Pembayaran atas nama **{dilayani.nama}** berhasil diproses.")
                st.info(f"Kasir telah sukses memindai {dilayani.jumlah_barang} item barang.")
                time.sleep(1.5)
                st.rerun()

# MENU 5: TENTANG APLIKASI
elif menu == "ℹ️ Tentang Aplikasi":
    st.markdown('<p class="main-title">ℹ️ Tentang Aplikasi</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-card">
        <h3>🧠 Konsep Struktur Data yang Digunakan:</h3>
        <ul>
            <li><b>Linked List:</b> Digunakan untuk alokasi memori antrean dinamis via objek Node.</li>
            <li><b>Queue (Antrean):</b> Memanfaatkan operasi <i>Enqueue</i> (Tambah) dan <i>Dequeue</i> (Layani) dengan aturan ketat <b>FIFO</b>.</li>
        </ul>
        <p style="font-size: 13px; color: #64748B; margin-top:20px;">Dibuat untuk keperluan tugas demonstrasi akademis.</p>
    </div>
    """, unsafe_allow_html=True)
