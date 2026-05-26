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

    # Menambahkan pelanggan ke antrean kasir (Enqueue)
    def tambah_pelanggan(self, nama, jumlah_barang):
        baru = PelangganNode(nama, jumlah_barang)
        if self.is_empty():
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru

    # Melayani pelanggan paling depan (Dequeue)
    def layani_pelanggan(self):
        if self.is_empty():
            return None
        
        pelanggan_dilayani = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
            
        self.total_pelanggan_dilayani += 1
        return pelanggan_dilayani

    # Mengonversi antrean menjadi teks rapi untuk ditampilkan di web
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

# Inisialisasi session state agar data antrean tidak hilang saat refresh/klik tombol
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()

antrean = st.session_state.antrean_kasir

# ==========================================
# SIDEBAR NAVIGATION (MENU UTAMA)
# ==========================================
st.sidebar.title("🏪 Navigasi Menu")
st.sidebar.write("Silakan pilih menu di bawah ini:")

# Membuat pilihan menu menggunakan radio button di sidebar
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "👥 Lihat Antrean", "➕ Tambah Pelanggan", "🧾 Proses Checkout", "ℹ️ Tentang Aplikasi"]
)

# Tombol Reset Sistem ditaruh di bawah menu sidebar agar rapi
st.sidebar.markdown("---")
if st.sidebar.button("🚨 Reset Sistem Kasir", type="secondary"):
    st.session_state.antrean_kasir = QueueSupermarket()
    st.success("Sistem berhasil direset!")
    time.sleep(1)
    st.rerun()


# ==========================================
# KONDISI LOGIKA UNTUK TIAP MENU
# ==========================================

# MENU 1: BERANDA
if menu == "🏠 Beranda":
    st.title("🛒 Selamat Datang di Simulasi Antrean Supermarket")
    st.subheader("Sistem Manajemen Antrean Kasir Berbasis Struktur Data Queue (FIFO)")
    st.write("")
    st.write("""
    Aplikasi ini dirancang untuk mensimulasikan bagaimana sebuah antrean di kasir supermarket berjalan.
    Dengan prinsip **First In, First Out (FIFO)**, pelanggan yang pertama kali mengantre akan menjadi yang pertama kali dilayani.
    """)
    
    # Menampilkan ringkasan status saat ini di Beranda
    st.markdown("### 📊 Status Kasir Saat Ini")
    panjang = 0
    curr = antrean.head
    while curr:
        panjang += 1
        curr = curr.next
        
    col1, col2 = st.columns(2)
    col1.metric("Pelanggan Menunggu", f"{panjang} Orang")
    col2.metric("Total Sukses Dilayani", f"{antrean.total_pelanggan_dilayani} Orang")

# MENU 2: LIHAT ANTREAN
elif menu == "👥 Lihat Antrean":
    st.title("👥 Kondisi Antrean Kasir Saat Ini")
    st.write("Berikut adalah daftar pelanggan yang sedang mengantre di meja kasir.")
    
    # Statistik Singkat
    col1, col2 = st.columns(2)
    with col1:
        panjang = 0
        curr = antrean.head
        while curr:
            panjang += 1
            curr = curr.next
        st.metric(label="Jumlah Antrean Sekarang", value=f"{panjang} Orang")
    with col2:
        st.metric(label="Total Pelanggan Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang")
    
    st.write("---")
    
    # Menampilkan visualisasi teks antrean
    antrean_teks = antrean.dapatkan_antrean_string()
    st.text_area("Daftar Antrean (Urutan teratas adalah yang terdepan):", value=antrean_teks, height=200, disabled=True)

# MENU 3: TAMBAH PELANGGAN
elif menu == "➕ Tambah Pelanggan":
    st.title("➕ Masukkan Pelanggan Baru")
    st.write("Gunakan formulir ini untuk menambahkan pelanggan yang baru selesai berbelanja ke dalam antrean.")
    
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

# MENU 4: PROSES CHECKOUT
elif menu == "🧾 Proses Checkout":
    st.title("🧾 Meja Kasir (Proses Pelayanan)")
    st.write("Menu khusus untuk kasir memproses pembayaran pelanggan satu per satu.")
    
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
    st.title("ℹ️ Tentang Aplikasi")
    st.write("""
    Aplikasi **Simulasi Antrean Checkout Supermarket** ini dibuat menggunakan bahasa pemrograman **Python** dan framework **Streamlit**.
    
    ### 🧠 Konsep Struktur Data yang Digunakan:
    * **Linked List:** Digunakan untuk mengalokasikan memori antrean secara dinamis (menggunakan `PelangganNode`).
    * **Queue (Antrean):** Menerapkan prinsip **FIFO (First In, First Out)** di mana elemen yang pertama kali masuk (`tambah_pelanggan`) akan menjadi elemen yang pertama kali keluar (`layani_pelanggan`).
    """)
