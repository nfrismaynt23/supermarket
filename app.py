import streamlit as st

# ==========================================
# KELAS QUEUE / ANTRIAN
# ==========================================
class Antrian:
    def __init__(self):
        self.queue = []

    # Tambah pelanggan
    def tambah_pelanggan(self, nama):
        self.queue.append(nama)

    # Layani pelanggan pertama
    def layani_pelanggan(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    # Cari posisi pelanggan
    def cari_pelanggan(self, nama):
        if nama in self.queue:
            return self.queue.index(nama) + 1
        return None

    # Reset semua antrian
    def reset_antrian(self):
        self.queue.clear()


# ==========================================
# SESSION STATE
# ==========================================
if "queue_obj" not in st.session_state:
    st.session_state.queue_obj = Antrian()

queue = st.session_state.queue_obj


# ==========================================
# JUDUL APLIKASI
# ==========================================
st.title("Sistem Antrian Supermarket")

# Membuat tab
tab1, tab2, tab3 = st.tabs([
    "Tambah Pelanggan",
    "Layani Pelanggan",
    "Cari Pelanggan"
])


# ==========================================
# TAB 1 - TAMBAH PELANGGAN
# ==========================================
with tab1:

    st.subheader("Tambah Pelanggan Baru")

    nama = st.text_input(
        "Masukkan nama pelanggan",
        key="input_tambah"
    )

    if st.button(
        "Tambah ke Antrian",
        key="btn_tambah"
    ):

        if nama.strip() != "":
            queue.tambah_pelanggan(nama)
            st.success(f"{nama} berhasil ditambahkan!")
        else:
            st.warning("Nama pelanggan wajib diisi!")


# ==========================================
# TAB 2 - LAYANI PELANGGAN
# ==========================================
with tab2:

    st.subheader("Layani Pelanggan")

    if st.button(
        "Layani Pelanggan Pertama",
        key="btn_layani"
    ):

        pelanggan = queue.layani_pelanggan()

        if pelanggan:
            st.success(f"{pelanggan} sedang dilayani")
        else:
            st.error("Antrian masih kosong!")


# ==========================================
# TAB 3 - CARI PELANGGAN
# ==========================================
with tab3:

    st.subheader("Cari Posisi Pelanggan")

    cari = st.text_input(
        "Masukkan nama pelanggan",
        key="input_cari"
    )

    if st.button(
        "Cari Posisi",
        key="btn_cari"
    ):

        posisi = queue.cari_pelanggan(cari)

        if posisi:
            st.success(
                f"{cari} berada di posisi antrian ke-{posisi}"
            )
        else:
            st.error("Pelanggan tidak ditemukan.")


# ==========================================
# TAMPILKAN ANTRIAN
# ==========================================
st.divider()

st.subheader("Daftar Antrian Saat Ini")

if len(queue.queue) > 0:

    nomor = 1

    for pelanggan in queue.queue:
        st.write(f"{nomor}. {pelanggan}")
        nomor += 1

else:
    st.warning("Belum ada antrian.")


# ==========================================
# RESET ANTRIAN
# ==========================================
st.divider()

if st.button(
    "Reset Semua Antrian",
    key="btn_reset"
):

    queue.reset_antrian()

    st.success("Semua antrian berhasil direset!")
