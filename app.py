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
st.set_page_config(page_title="Novriah SmartMart System", page_icon="🛒", layout="wide")

# --- CUSTOM CSS: GRADIENT WARNA DAN CARD EMAS/BIRU ---
custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%) !important;
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
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-left: 6px solid #38bdf8 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INISIALISASI DATA ---
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []
if 'data_produk' not in st.session_state:
    st.session_state.data_produk = [
        "PRD01 - Susu UHT Kotak (Rp 18.500)",
        "PRD02 - Mie Instan Cup (Rp 5.000)",
        "PRD03 - Minyak Goreng 2L (Rp 36.000)",
        "PRD04 - Roti Gandum Kasur (Rp 15.000)"
    ]

antrean = st.session_state.antrean_kasir

# ==========================================
# GERBANG 1: HALAMAN LOGIN (DENGAN LOGO KAMPUS)
# ==========================================
if not st.session_state.is_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.3, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:40px; margin-bottom:10px;">', unsafe_allow_html=True)
        
        # LINK LOGO KAMPUS (Ganti URL di bawah ini dengan link gambar logo Global Institute kamu jika punya)
        logo_url = "https://global.ac.id/wp-content/uploads/2021/01/logo-global-80.png"
        st.image(logo_url, width=160)
        
        st.markdown('<h1 style="color: #38bdf8; font-size: 32px; margin-bottom:0px;">Sign In NOVRIAH SMARTMART</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 14px;">Integrated Academic & Cashier Information System</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username / NIK Pegawai:")
        password = st.text_input("Password:", type="password")
        
        if st.button("Log In Ke Sistem 🚀", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Username atau Password salah! (Hint: admin / 123)")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# GERBANG 2: DASHBOARD UTAMA (SETELAH LOGIN)
# ==========================================
else:
    # Nama toko muncul juga di atas menu navigasi samping
    st.sidebar.markdown("<h2 style='color:#38bdf8 !important; margin-bottom:0;'>🛒 Novriah SmartMart</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#94a3b8; font-size:12px; margin-top:0;'>Kasir: Admin Active</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Pilih Halaman Kerja:",
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
        st.markdown('<h1 style="color: #38bdf8;">🏪 Selamat Datang di Novriah SmartMart</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="clean-box">
            <h4>💡 Aturan Algoritma Antrean (Queue)</h4>
            <p>Sistem pada toko <b>Novriah SmartMart</b> dijalankan secara ketat menggunakan metode <b>FIFO (First In First Out)</b>. Pembeli yang mengantre paling awal wajib diselesaikan transaksinya terlebih dahulu sebelum melayani pembeli di belakangnya.</p>
        </div>
        """, unsafe_allow_html=True)
        
        panjang = 0
        curr = antrean.head
        while curr:
            panjang += 1
            curr = curr.next
            
        st.write(f"### 🔴 Antrean Menunggu di Kasir: **{panjang} Orang**")
        st.write(f"### 🟢 Sukses Transaksi Hari Ini: **{antrean.total_pelanggan_dilayani} Orang**")

    # MENU 2: LIHAT DAFTAR PRODUK
    elif menu == "🛍️ Lihat Daftar Produk":
        st.markdown('<h1 style="color: #38bdf8;">🛍️ Katalog Produk Toko</h1>', unsafe_allow_html=True)
        st.write("Daftar barang aktif di etalase Novriah SmartMart:")
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        for produk in st.session_state.data_produk:
            st.write(f"🔸 {produk}")
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 3: LIHAT ANTREAN KASIR
    elif menu == "👥 Lihat Antrean Kasir":
        st.markdown('<h1 style="color: #38bdf8;">👥 Barisan Antrean Real-Time</h1>', unsafe_allow_html=True)
        antrean_teks = antrean.dapatkan_antrean_string()
        st.text_area("Urutan Barisan Kasir:", value=antrean_teks, height=200, disabled=True)

    # MENU 4: TAMBAH PELANGGAN BARU
    elif menu == "➕ Tambah Pelanggan Baru":
        st.markdown('<h1 style="color: #38bdf8;">➕ Registrasi Pelanggan Masuk Antrean</h1>', unsafe_allow_html=True)
        
        with st.form("form_tambah"):
            nama = st.text_input("Nama Pelanggan:")
            barang = st.number_input("Jumlah Barang Belanjaan:", min_value=1, value=5)
            if st.form_submit_button("Dorong ke Antrean"):
                if nama.strip():
                    antrean.tambah_pelanggan(nama, barang)
                    st.success(f"Pelanggan '{nama}' masuk barisan kasir!")
                else:
                    st.warning("Nama wajib diisi!")

    # MENU 5: PROSES CHECKOUT
    elif menu == "🧾 Proses Kasir (Checkout)":
        st.markdown('<h1 style="color: #38bdf8;">🧾 Meja Pembayaran & Nota Transaksi</h1>', unsafe_allow_html=True)
        
        if antrean.is_empty():
            st.info("Tidak ada antrean pembeli saat ini.")
        else:
            pelanggan_depan = antrean.head
            total_harga = pelanggan_depan.jumlah_barang * 15000
            
            st.write(f"### Pelanggan Terdepan: **{pelanggan_depan.nama}**")
            st.write(f"Membawa: {pelanggan_depan.jumlah_barang} item barang")
            st.write(f"### 💰 Total Nota Pembayaran: **Rp {total_harga:,}**")
            
            if st.button("Cetak Struk & Selesai", type="primary"):
                dilayani = antrean.layani_pelanggan()
                if dilayani:
                    catatan = f"Pelanggan {dilayani.nama} sukses membayar {dilayani.jumlah_barang} barang seharga Rp {total_harga:,}"
                    st.session_state.riwayat_transaksi.append(catatan)
                    st.success("Nota sukses dicetak dan dikeluarkan dari antrean!")
                    st.rerun()

    # MENU 6: RIWAYAT TRANSAKSI KELUAR
    elif menu == "📊 Riwayat Transaksi Keluar":
        st.markdown('<h1 style="color: #38bdf8;">📊 Jurnal Transaksi Sukses</h1>', unsafe_allow_html=True)
        
        if not st.session_state.riwayat_transaksi:
            st.info("Belum ada transaksi keluar.")
        else:
            st.markdown('<div class="clean-box">', unsafe_allow_html=True)
            for item in st.session_state.riwayat_transaksi:
                st.write(f"✅ {item}")
            st.markdown('</div>', unsafe_allow_html=True)
