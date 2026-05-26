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

# --- CUSTOM CSS: BACKGROUND MALL MODERN & ANTI-HITAM ---
custom_css = """
<style>
    /* Mengunci background dengan gambar interior supermarket di dalam mall/gedung modern */
    .stApp {
        background: linear-gradient(rgba(248, 250, 252, 0.88), rgba(248, 250, 252, 0.88)), 
                    url('https://images.unsplash.com/photo-1534723452862-4c874018d66d?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* MEMAKSA semua teks berwarna gelap tajam (Anti tenggelam / anti hitam semua) */
    h1, h2, h3, h4, p, span, label, th, td, li {
        color: #0F172A !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Judul Utama */
    .title-premium {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important; /* Biru Navy Premium */
        margin-bottom: 2px !important;
    }
    
    .subtitle-premium {
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        margin-bottom: 30px !important;
    }

    /* Box Informasi Putih Solid agar kontras dengan background */
    .clean-box {
        background-color: #FFFFFF !important;
        border-left: 6px solid #2563EB !important;
        border-radius: 12px !important;
        padding: 22px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 25px !important;
    }
    
    /* Kotak Angka Merah Halus */
    .card-wait {
        background-color: #FFF5F5 !important;
        border: 1px solid #FEB2B2 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* Kotak Angka Hijau Halus */
    .card-success {
        background-color: #F0FDF4 !important;
        border: 1px solid #9AE6B4 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
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
    st.markdown('<h1 class="title-premium">🛒 Selamat Datang di Simulasi Antrean Supermarket</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-premium">Sistem Manajemen Antrean Kasir Berbasis Struktur Data Queue (FIFO)</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="clean-box">
        <h4 style="margin-top:0; color:#1E3A8A !important; font-weight:700;">💡 Alur Kerja Antrean Kasir</h4>
        <p style="margin:0; font-size:15px; line-height:1.6;">
            Aplikasi ini mensimulasikan kasir pusat belanja besar di dalam gedung/mall secara riil. 
            Menerapkan metode <b>First In, First Out (FIFO)</b>, di mana setiap pelanggan baru yang datang 
            akan mengantre di belakang, dan kasir akan menyelesaikan belanjaan dari orang yang berada di barisan paling depan terlebih dahulu.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-weight:700; margin-bottom:15px;'>📊 Ringkasan Status Meja Kasir</h3>", unsafe_allow_html=True)
    
    panjang = 0
    curr = antrean.head
    while curr:
        panjang += 1
        curr = curr.next
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card-wait">
            <p style="margin:0; font-size:15px; font-weight:600; color:#991B1B !important;">Pelanggan Menunggu Saat Ini</p>
            <p style="margin:5px 0 0 0; font-size:38px; font-weight:800; color:#E53E3E !important;">{panjang} Orang</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="card-success">
            <p style="margin:0; font-size:15px; font-weight:600; color:#166534 !important;">Total Sukses Dilayani</p>
            <p style="margin:5px 0 0 0; font-size:38px; font-weight:800; color:#38A169 !important;">{antrean.total_pelanggan_dilayani} Orang</p>
        </div>
        """, unsafe_allow_html=True)

# MENU 2: LIHAT ANTREAN
elif menu == "👥 Lihat Antrean":
    st.markdown('<h1 class="title-premium">👥 Kondisi Antrean Kasir Saat Ini</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-premium">Daftar urutan pelanggan yang sedang mengantre di kasir</p>', unsafe_allow_html=True)
    
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
    st.text_area("Urutan Antrean (Baris paling atas adalah antrean terdepan):", value=antrean_teks, height=250, disabled=True)

# MENU 3: TAMBAH PELANGGAN
elif menu == "➕ Tambah Pelanggan":
    st.markdown('<h1 class="title-premium">➕ Masukkan Pelanggan Baru</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-premium">Tambahkan data pelanggan yang baru menuju kasir</p>', unsafe_allow_html=True)
    
    with st.form("form_pelanggan", clear_on_submit=True):
        nama_pelanggan = st.text_input("Nama Pelanggan:")
        jumlah_item = st.number_input("Jumlah Barang Belanjaan:", min_value=1, max_value=100, value=5)
        submit_button = st.form_submit_button("Masuk Antrean", type="primary")
        
        if submit_button:
            if nama_pelanggan.strip():
                antrean.tambah_pelanggan(nama_pelanggan, jumlah_item)
                st.success(f"🛒 Pelanggan '{nama_pelanggan}' dengan membawa {jumlah_item} barang berhasil masuk ke antrean!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Harap masukkan nama pelanggan terlebih dahulu.")

# MENU 4: PROSES CHECKOUT
elif menu == "🧾 Proses Checkout":
    st.markdown('<h1 class="title-premium">🧾 Meja Kasir (Proses Pelayanan)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-premium">Lokasi pemrosesan transaksi pembayaran belanja</p>', unsafe_allow_html=True)
    
    if antrean.is_empty():
        st.info("🎉 Semua antrean sudah selesai diproses. Kasir sedang kosong!")
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
    st.markdown('<h1 class="title-premium">ℹ️ Tentang Aplikasi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-premium">Detail teknis sistem aplikasi simulasi kasir</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🧠 Landasan Teori Struktur Data")
        st.markdown("- **Linked List (Pointer):** Setiap elemen antrean dibentuk dari kelas `PelangganNode` yang menyimpan referensi ke elemen setelahnya (*Dynamic Memory Allocation*).")
        st.markdown("- **Queue (Antrean):** Struktur data linier yang bekerja secara **First In First Out (FIFO)**. Operasi penambahan dilakukan di bagian belakang (*Tail*) dan pengurangan dilakukan di bagian depan (*Head*).")
        st.caption("Dibuat untuk keperluan tugas demonstrasi akademis.")
