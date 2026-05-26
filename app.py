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
    st.title("🛒 Selamat Datang di Simulasi Antrean Supermarket")
    st.write("Sistem Manajemen Antrean Kasir Berbasis Struktur Data Queue (FIFO)")
    
    # Menggunakan border kontainer bawaan agar aman di dark/light mode
    with st.container(border=True):
        st.subheader("💡 Cara Kerja Sistem (Struktur Data Queue)")
        st.write(
            "Aplikasi ini mensimulasikan alur pelayanan kasir di sebuah market secara riil. "
            "Menggunakan metode **First In, First Out (FIFO)**, pelanggan yang pertama kali mengantre "
            "akan diprioritaskan untuk dilayani terlebih dahulu sebelum pelanggan yang datang setelahnya."
        )
    
    st.write("")
    st.subheader("📊 Ringkasan Status Meja Kasir")
    
    # Hitung data antrean saat ini
    panjang = 0
    curr = antrean.head
    while curr:
        panjang += 1
        curr = curr.next
        
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric(label="Pelanggan Menunggu Saat Ini", value=f"{panjang} Orang", delta="- Menunggu")
        
    with col2:
        with st.container(border=True):
            st.metric(label="Total Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang", delta="✅ Sukses", delta_color="inverse")

# MENU 2: LIHAT ANTREAN
elif menu == "👥 Lihat Antrean":
    st.title("👥 Kondisi Antrean Kasir Saat Ini")
    st.write("Daftar urutan pelanggan yang sedang mengantre di kasir")
    
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
    st.title("➕ Masukkan Pelanggan Baru")
    st.write("Tambahkan data pelanggan yang baru menuju kasir")
    
    with st.form("form_pelanggan", clear_on_submit=True):
        nama_pelanggan = st.text_input("Nama Pelanggan:")
        jumlah_item = st.number_input("Jumlah Barang Belanjaan:", min_value=1, max_value=100, value=5)
        submit_button = st.form_submit_button("Masukkan ke Antrean", type="primary")
        
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
    st.title("🧾 Meja Kasir (Proses Pelayanan)")
    st.write("Lokasi pemrosesan transaksi pembayaran belanja")
    
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
    st.title("ℹ️ Tentang Aplikasi")
    st.write("Detail teknis sistem aplikasi simulasi kasir")
    
    with st.container(border=True):
        st.subheader("🧠 Landasan Teori Struktur Data")
        st.markdown("- **Linked List (Pointer):** Setiap elemen antrean dibentuk dari kelas `PelangganNode` yang menyimpan referensi ke elemen setelahnya (*Dynamic Memory Allocation*).")
        st.markdown("- **Queue (Antrean):** Struktur data linier yang bekerja secara **First In First Out (FIFO)**. Operasi penambahan dilakukan di bagian belakang (*Tail*) dan pengurangan dilakukan di bagian depan (*Head*).")
        st.caption("Dibuat untuk keperluan tugas demonstrasi akademis.")
