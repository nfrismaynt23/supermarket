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
st.set_page_config(page_title="Checkout Supermarket", page_icon="🛒")

st.title("🛒 Simulasi Antrean Checkout Supermarket")
st.write("Aplikasi interaktif simulasi pelayanan kasir dengan struktur data Queue (FIFO).")

# Inisialisasi session state agar data antrean tidak hilang saat refresh/klik tombol
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()

antrean = st.session_state.antrean_kasir

# Sistem Tab sesuai dengan referensi file app (1).py
tab1, tab2, tab3 = st.tabs(["👥 Lihat Antrean", "➕ Pelanggan Baru", "🧾 Proses Checkout"])

# TAB 1: Lihat Antrean Saat Ini
with tab1:
    st.subheader("Kondisi Antrean Kasir Saat Ini")
    
    # Statistik Singkat
    col1, col2 = st.columns(2)
    with col1:
        # Menghitung panjang antrean manual
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
    st.code(antrean_teks, language="text")

# TAB 2: Menambahkan Pelanggan Baru (Enqueue)
with tab2:
    st.subheader("Masukkan Pelanggan ke Antrean")
    nama_pelanggan = st.text_input("Nama Pelanggan:")
    jumlah_item = st.number_input("Jumlah Barang Belanjaan:", min_value=1, max_value=100, value=5)
    
    if st.button("Masuk Antrean", type="primary"):
        if nama_pelanggan.strip():
            antrean.tambah_pelanggan(nama_pelanggan, jumlah_item)
            st.success(f"🛒 '{nama_pelanggan}' (membawa {jumlah_item} barang) berhasil masuk ke antrean kasir!")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Harap masukkan nama pelanggan terlebih dahulu.")

# TAB 3: Proses Checkout (Dequeue)
with tab3:
    st.subheader("Meja Kasir (Pelayanan)")
    
    if antrean.is_empty():
        st.info("Tidak ada pelanggan di dalam antrean saat ini.")
    else:
        pelanggan_depan = antrean.head
        st.warning(f"Pelanggan berikutnya yang akan dilayani: **{pelanggan_depan.nama}** ({pelanggan_depan.jumlah_barang} barang).")
        
        if st.button("Proses & Selesaikan Pembayaran"):
            # Proses dequeue
            dilayani = antrean.layani_pelanggan()
            if dilayani:
                st.success(f"✅ Selesai! Pembayaran atas nama **{dilayani.nama}** berhasil diproses.")
                st.info(f"Kasir telah sukses memindai {dilayani.jumlah_barang} item barang.")
                time.sleep(1.5)
                st.rerun()

# Tombol Reset Sistem
st.divider()
if st.button("Reset Sistem / Kosongkan Kasir"):
    st.session_state.antrean_kasir = QueueSupermarket()
    st.rerun()
