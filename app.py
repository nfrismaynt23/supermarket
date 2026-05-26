import streamlit as st

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
st.set_page_config(page_title="Sistem Kasir Supermarket", page_icon="🛒", layout="wide")

# --- CUSTOM CSS: WARNA BACKGROUND MENARIK (ANTI-KOSONG) ---
custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 2px solid #3b82f6 !important;
    }
    h1, h2, h3, h4, p, span, label, li, div {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    [data-testid="stWidgetLabel"] p, .st-dc, .st-da, .st-db {
        color: #ffffff !important;
    }
    .clean-box {
        background: rgba(255, 255, 255, 0.1) !important;
        border-left: 6px solid #38bdf8 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INISIALISASI DATA KASIR ---
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []
if 'data_produk' not in st.session_state:
    # Menggunakan list biasa agar mudah dijelaskan tanpa library pandas
    st.session_state.data_produk = [
        "PRD01 - Susu UHT Kotak (Rp 18.500)",
        "PRD02 - Mie Instan Cup (Rp 5.000)",
        "PRD03 - Minyak Goreng 2L (Rp 36.000)",
        "PRD04 - Roti Gandum Kasur (Rp 15.000)"
    ]

antrean = st.session_state.antrean_kasir

# ==========================================
# GERBANG 1: HALAMAN LOGIN
# ==========================================
if not st.session_state.is_logged_in:
    st.markdown('<div style="text-align:center; margin-top:60px;">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #38bdf8;">🔓 MENU LOGIN KASIR SUPERMARKET</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        
        if st.button("Masuk Sistem Kasir 🚀", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Username atau Password salah! (Hint: admin / 123)")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# GERBANG 2: HALAMAN UTAMA (SETELAH LOGIN)
# ==========================================
else:
    st.sidebar.markdown("<h2 style='color:#38bdf8 !important;'>🏪 Menu Navigasi</h2>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio(
        "Pilih Halaman:",
        [
            "🏠 Beranda Utama", 
            "🛍️ Lihat Daftar Produk",
            "👥 Lihat Antrean Kasir", 
            "➕ Tambah Pelanggan Baru", 
            "🧾 Proses Kasir (Checkout)", 
            "📊 Riwayat Transaksi Keluar"
        ]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Keluar / Logout", type="primary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()

    # MENU 1: BERANDA
    if menu == "🏠 Beranda Utama":
        st.markdown('<h1 style="color: #38bdf8;">🛒 Dashboard Antrean Kasir</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="clean-box">
            <h4>💡 Cara Kerja Struktur Data Antrean (Queue)</h4>
            <p>Program ini dibuat menggunakan metode <b>FIFO (First In First Out)</b>. Pelanggan yang pertama kali dimasukkan ke antrean akan menjadi orang yang pertama kali dilayani oleh kasir.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hitung panjang antrean manual tanpa library tambahan
        panjang = 0
        curr = antrean.head
        while curr:
            panjang += 1
            curr = curr.next
            
        st.write(f"### 🔴 Pelanggan Menunggu Saat Ini: **{panjang} Orang**")
        st.write(f"### 🟢 Total Pelanggan Sukses Dilayani: **{antrean.total_pelanggan_dilayani} Orang**")

    # MENU 2: LIHAT DAFTAR PRODUK
    elif menu == "🛍️ Lihat Daftar Produk":
        st.markdown('<h1 style="color: #38bdf8;">🛍️ Daftar Produk Toko</h1>', unsafe_allow_html=True)
        st.write("Berikut adalah daftar master barang yang tersedia di supermarket:")
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        for produk in st.session_state.data_produk:
            st.write(f"- {produk}")
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 3: LIHAT ANTREAN KASIR
    elif menu == "👥 Lihat Antrean Kasir":
        st.markdown('<h1 style="color: #38bdf8;">👥 Urutan Barisan Antrean</h1>', unsafe_allow_html=True)
        antrean_teks = antrean.dapatkan_antrean_string()
        st.text_area("Daftar Urutan (Paling atas berarti antrean terdepan):", value=antrean_teks, height=200, disabled=True)

    # MENU 4: TAMBAH PELANGGAN BARU
    elif menu == "➕ Tambah Pelanggan Baru":
        st.markdown('<h1 style="color: #38bdf8;">➕ Tambah Pelanggan Ke Antrean</h1>', unsafe_allow_html=True)
        
        with st.form("form_tambah"):
            nama = st.text_input("Nama Pelanggan:")
            barang = st.number_input("Jumlah Barang Belanjaan:", min_value=1, value=5)
            if st.form_submit_button("Masukkan Ke Antrean"):
                if nama.strip():
                    antrean.tambah_pelanggan(nama, barang)
                    st.success(f"Pelanggan '{nama}' berhasil masuk antrean!")
                else:
                    st.warning("Nama tidak boleh kosong!")

    # MENU 5: PROSES CHECKOUT
    elif menu == "🧾 Proses Kasir (Checkout)":
        st.markdown('<h1 style="color: #38bdf8;">🧾 Meja Pembayaran Kasir</h1>', unsafe_allow_html=True)
        
        if antrean.is_empty():
            st.info("Antrean kosong! Kasir sedang tidak melayani siapapun.")
        else:
            pelanggan_depan = antrean.head
            total_harga = pelanggan_depan.jumlah_barang * 15000
            
            st.write(f"### Pelanggan Terdepan: **{pelanggan_depan.nama}**")
            st.write(f"Bawaan: {pelanggan_depan.jumlah_barang} barang")
            st.write(f"### 💰 Total Tagihan: **Rp {total_harga:,}**")
            
            if st.button("Selesaikan Transaksi", type="primary"):
                dilayani = antrean.layani_pelanggan()
                if dilayani:
                    # Simpan catatan string sederhana ke list riwayat
                    catatan = f"Pelanggan {dilayani.nama} membeli {dilayani.jumlah_barang} barang (Total: Rp {total_harga:,})"
                    st.session_state.riwayat_transaksi.append(catatan)
                    st.success("Transaksi sukses diproses!")
                    st.rerun()

    # MENU 6: RIWAYAT TRANSAKSI KELUAR
    elif menu == "📊 Riwayat Transaksi Keluar":
        st.markdown('<h1 style="color: #38bdf8;">📊 Riwayat Transaksi Hari Ini</h1>', unsafe_allow_html=True)
        
        if not st.session_state.riwayat_transaksi:
            st.info("Belum ada transaksi pembayaran yang selesai.")
        else:
            st.markdown('<div class="clean-box">', unsafe_allow_html=True)
            for item in st.session_state.riwayat_transaksi:
                st.write(f"✅ {item}")
            st.markdown('</div>', unsafe_allow_html=True)
