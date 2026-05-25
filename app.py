import streamlit as st

# ==========================================
# KELAS QUEUE CHECKOUT SUPERMARKET
# ==========================================
class CheckoutQueue:
    def __init__(self):
        self.antrian = []

    # Tambah pelanggan ke antrian
    def tambah_pelanggan(self, nama):
        self.antrian.append(nama)

    # Layani pelanggan pertama
    def layani_pelanggan(self):
        if len(self.antrian) > 0:
            return self.antrian.pop(0)
        return None

    # Lihat antrian sekarang
    def lihat_antrian(self):
        return self.antrian

    # Cari posisi pelanggan
    def cari_pelanggan(self, nama):
        if nama in self.antrian:
            return self.antrian.index(nama) + 1
        return None


# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(
    page_title="Checkout Supermarket",
    page_icon="🛒"
)

st.title("🛒 Checkout Supermarket")
st.write("Simulasi antrian kasir supermarket menggunakan struktur data Queue.")

# Session state supaya data tidak hilang
if 'checkout' not in st.session_state:
    st.session_state.checkout = CheckoutQueue()

queue = st.session_state.checkout

# ==========================================
# MENU TAB
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📋 Lihat Antrian",
    "➕ Tambah Pelanggan",
    "🔍 Cari Pelanggan"
])

# ==========================================
# TAB 1 - LIHAT ANTRIAN
# ==========================================
with tab1:
    st.subheader("Daftar Antrian Kasir")

    data_antrian = queue.lihat_antrian()

    if len(data_antrian) == 0:
        st.info("Belum ada pelanggan dalam antrian.")
    else:
        for i, pelanggan in enumerate(data_antrian, start=1):
            st.write(f"{i}. {pelanggan}")

    st.divider()

    if st.button("Layani Pelanggan Pertama"):
        hasil = queue.layani_pelanggan()

        if hasil:
            st.success(f"Pelanggan '{hasil}' selesai checkout.")
        else:
            st.error("Antrian masih kosong!")

# ==========================================
# TAB 2 - TAMBAH PELANGGAN
# ==========================================
with tab2:
    st.subheader("Tambah Pelanggan Baru")

    nama = st.text_input("Masukkan nama pelanggan")

    if st.button("Tambah ke Antrian"):
        if nama:
            queue.tambah_pelanggan(nama)
            st.success(f"Pelanggan '{nama}' berhasil masuk antrian.")
        else:
            st.warning("Nama pelanggan wajib diisi!")

# ==========================================
# TAB 3 - CARI PELANGGAN
# ==========================================
with tab3:
    st.subheader("Cari Posisi Pelanggan")

    cari = st.text_input("Masukkan nama pelanggan")

    if st.button("Cari Posisi"):
        posisi = queue.cari_pelanggan(cari)

        if posisi:
            st.success(f"{cari} berada di posisi antrian ke-{posisi}")
        else:
            st.error("Pelanggan tidak ditemukan.")

# ==========================================
# RESET
# ==========================================
st.divider()

if st.button("Reset Semua Antrian"):
    st.session_state.checkout = CheckoutQueue()
    st.rerun()