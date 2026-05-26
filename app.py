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
            return "Antrean Kosong"
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

# --- INISIALISASI DATA KASIR ---
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
# HALAMAN 1: LOGIN (BERSIH & FORMAL)
# ==========================================
if not st.session_state.is_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:60px; margin-bottom:20px;">', unsafe_allow_html=True)
        
        # Mengambil logo kampus secara formal
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

    # MENU 1: BERANDA
    if menu == "Beranda Utama":
        st.markdown('<h2>Dashboard Utama</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="clean-box">
            <h4 style="margin-top:0; color: #38bdf8;">Konsep Struktur Data Queue (FIFO)</h4>
            <p style="color: #94a3b8; font-size: 14px; margin-bottom:0;">
                Program ini mensimulasikan manajemen pelayanan kasir berdasarkan prinsip First In First Out. 
                Data dikelola menggunakan Linked List dinamis untuk melacak kedatangan pelanggan secara sistematis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        panjang = 0
        curr = antrean.head
        while curr:
            panjang += 1
            curr = curr.next
            
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.metric("Jumlah Antrean Menunggu", f"{panjang} Orang")
        with col_b2:
            st.metric("Total Pelanggan Terlayani", f"{antrean.total_pelanggan_dilayani} Orang")

    # MENU 2: LIHAT DAFTAR PRODUK
    elif menu == "Daftar Produk Toko":
        st.markdown('<h2>Katalog Produk Aktif</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        for produk in st.session_state.data_produk:
            st.markdown(f"<p style='font-size:15px; margin-bottom:6px;'>• {produk}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 3: LIHAT ANTREAN KASIR
    elif menu == "Monitor Antrean":
        st.markdown('<h2>Urutan Barisan Pelanggan</h2>', unsafe_allow_html=True)
        antrean_teks = antrean.dapatkan_antrean_string()
        st.text_area("Data Node Memori saat ini (FIFO):", value=antrean_teks, height=200, disabled=True)

    # MENU 4: TAMBAH PELANGGAN BARU
    elif menu == "Tambah Pelanggan Baru":
        st.markdown('<h2>Registrasi Kedatangan Pelanggan</h2>', unsafe_allow_html=True)
        
        with st.form("form_tambah"):
            nama = st.text_input("Nama Pelanggan:")
            barang = st.number_input("Jumlah Barang di Keranjang:", min_value=1, value=5)
            if st.form_submit_button("Masukkan ke Antrean"):
                if nama.strip():
                    antrean.tambah_pelanggan(nama, barang)
                    st.success("Data berhasil didaftarkan ke dalam sistem.")
                else:
                    st.warning("Kolom nama wajib diisi.")

    # MENU 5: PROSES CHECKOUT
    elif menu == "Proses Pembayaran (Checkout)":
        st.markdown('<h2>Meja Transaksi Utama</h2>', unsafe_allow_html=True)
        
        if antrean.is_empty():
            st.info("Sistem siap. Tidak ada antrean pelanggan saat ini.")
        else:
            pelanggan_depan = antrean.head
            total_harga = pelanggan_depan.jumlah_barang * 15000
            
            st.write(f"Pelanggan Terdepan: **{pelanggan_depan.nama}**")
            st.write(f"Beban Belanja: {pelanggan_depan.jumlah_barang} unit item")
            st.write(f"### Total Invoice: **Rp {total_harga:,}**")
            
            if st.button("Selesaikan Pembayaran", type="primary"):
                dilayani = antrean.layani_pelanggan()
                if dilayani:
                    catatan = f"Pelanggan {dilayani.nama} • {dilayani.jumlah_barang} item • Rp {total_harga:,} [Selesai]"
                    st.session_state.riwayat_transaksi.append(catatan)
                    st.success("Transaksi berhasil diproses.")
                    st.rerun()

    # MENU 6: RIWAYAT TRANSAKSI KELUAR
    elif menu == "Riwayat Jurnal Transaksi":
        st.markdown('<h2>Jurnal Rekap Transaksi</h2>', unsafe_allow_html=True)
        
        if not st.session_state.riwayat_transaksi:
            st.info("Jurnal transaksi harian masih kosong.")
        else:
            st.markdown('<div class="clean-box">', unsafe_allow_html=True)
            for item in st.session_state.riwayat_transaksi:
                st.markdown(f"<p style='color: #10b981 !important;'>✓ {item}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
