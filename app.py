import streamlit as stimport streamlit as st
from collections import deque
import time
import random
from datetime import datetime

# ==============================================
# STRUKTUR DATA: QUEUE (ANTRIAN)
# ==============================================

class Pelanggan:
    def __init__(self, nama, jumlah_item, metode_bayar, kategori):
        self.id = f"TKT-{random.randint(1000, 9999)}"
        self.nama = nama
        self.jumlah_item = jumlah_item
        self.metode_bayar = metode_bayar
        self.kategori = kategori  # "express" or "reguler"
        self.waktu_masuk = datetime.now().strftime("%H:%M:%S")
        self.waktu_masuk_dt = datetime.now()
        self.estimasi_detik = jumlah_item * 3  # 3 detik per item

    def lama_menunggu(self):
        selisih = (datetime.now() - self.waktu_masuk_dt).seconds
        menit = selisih // 60
        detik = selisih % 60
        return f"{menit}m {detik}s"

    def harga_estimasi(self):
        return self.jumlah_item * random.randint(10000, 50000)


class KasirQueue:
    def __init__(self, kasir_id, nama_kasir, tipe="reguler"):
        self.kasir_id = kasir_id
        self.nama_kasir = nama_kasir
        self.tipe = tipe  # "express" atau "reguler"
        self.antrian = deque()
        self.total_dilayani = 0
        self.total_pendapatan = 0
        self.status = "Buka"  # Buka / Tutup / Istirahat
        self.rata_waktu_layanan = []

    def enqueue(self, pelanggan):
        self.antrian.append(pelanggan)

    def dequeue(self):
        if not self.is_empty():
            pelanggan = self.antrian.popleft()
            self.total_dilayani += 1
            estimasi = pelanggan.harga_estimasi()
            self.total_pendapatan += estimasi
            lama = (datetime.now() - pelanggan.waktu_masuk_dt).seconds
            self.rata_waktu_layanan.append(lama)
            return pelanggan, estimasi
        return None, 0

    def peek(self):
        if not self.is_empty():
            return self.antrian[0]
        return None

    def is_empty(self):
        return len(self.antrian) == 0

    def size(self):
        return len(self.antrian)

    def total_item(self):
        return sum(p.jumlah_item for p in self.antrian)

    def estimasi_menit(self):
        total_detik = sum(p.estimasi_detik for p in self.antrian)
        return max(1, total_detik // 60)

    def daftar(self):
        return list(self.antrian)

    def avg_waktu_layanan(self):
        if not self.rata_waktu_layanan:
            return 0
        return sum(self.rata_waktu_layanan) // len(self.rata_waktu_layanan)

    def beban(self):
        if self.size() == 0:
            return "Kosong"
        elif self.size() <= 3:
            return "Ringan"
        elif self.size() <= 6:
            return "Sedang"
        else:
            return "Padat"


# ==============================================
# KONFIGURASI HALAMAN & STYLING
# ==============================================

st.set_page_config(
    page_title="SuperMart Queue System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --bg-deep: #0a0e1a;
    --bg-card: #111827;
    --bg-card2: #1a2235;
    --accent: #f97316;
    --accent2: #fbbf24;
    --green: #10b981;
    --red: #ef4444;
    --blue: #3b82f6;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --border: #1e293b;
}

/* ---- GLOBAL BACKGROUND ---- */
.stApp {
    background: 
        radial-gradient(ellipse at 10% 20%, rgba(249,115,22,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(59,130,246,0.10) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(251,191,36,0.05) 0%, transparent 70%),
        linear-gradient(160deg, #0a0e1a 0%, #0d1321 40%, #0a0e1a 100%);
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* ---- HEADER ---- */
.hero-header {
    background: linear-gradient(135deg, rgba(249,115,22,0.15), rgba(251,191,36,0.08));
    border: 1px solid rgba(249,115,22,0.3);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(249,115,22,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 6px 0;
    line-height: 1.1;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin: 0;
    font-weight: 300;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #10b981;
    font-weight: 600;
    margin-top: 10px;
}
.live-dot {
    width: 7px;
    height: 7px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ---- METRIC CARDS ---- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.orange::after { background: linear-gradient(90deg, #f97316, #fbbf24); }
.metric-card.green::after  { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-card.blue::after   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.metric-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); }
.metric-label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: var(--text); line-height: 1; }
.metric-icon  { font-size: 1.6rem; position: absolute; top: 16px; right: 16px; opacity: 0.5; }

/* ---- KASIR CARDS ---- */
.kasir-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}
.kasir-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    transition: border-color 0.2s;
}
.kasir-card:hover { border-color: rgba(249,115,22,0.4); }
.kasir-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}
.kasir-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
}
.badge {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
}
.badge-express  { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-reguler  { background: rgba(59,130,246,0.15);  color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.badge-buka     { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-tutup    { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.badge-istirahat{ background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }

.kasir-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 14px 0;
}
.stat-mini {
    background: var(--bg-card2);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 0.8rem;
}
.stat-mini span { color: var(--muted); display: block; font-size: 0.7rem; margin-bottom: 2px; }

/* ---- ANTRIAN LIST ---- */
.antrian-wrapper { margin-top: 12px; }
.antrian-item {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    margin: 5px 0;
    font-size: 0.82rem;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.antrian-item.first {
    background: linear-gradient(135deg, rgba(249,115,22,0.2), rgba(251,191,36,0.1));
    border-color: rgba(249,115,22,0.4);
    color: var(--text);
}
.antrian-nama { font-weight: 600; color: var(--text); }
.antrian-info { font-size: 0.72rem; color: var(--muted); }
.progress-bar-wrap { background: var(--border); border-radius: 4px; height: 4px; margin-top: 8px; }
.progress-bar-fill {
    height: 4px;
    border-radius: 4px;
    background: linear-gradient(90deg, #f97316, #fbbf24);
    transition: width 0.3s;
}
.empty-state { text-align: center; padding: 20px; color: var(--muted); font-size: 0.85rem; }

/* ---- FORM SECTION ---- */
.form-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

/* ---- LOG ITEM ---- */
.log-item {
    background: var(--bg-card2);
    border-left: 3px solid;
    border-radius: 0 8px 8px 0;
    padding: 8px 14px;
    margin: 5px 0;
    font-size: 0.8rem;
    font-family: 'DM Mono', monospace;
}
.log-item.enqueue { border-color: #10b981; }
.log-item.dequeue { border-color: #f97316; }
.log-item.status  { border-color: #3b82f6; }
.log-item.reset   { border-color: #ef4444; }
.log-time { color: var(--muted); margin-right: 8px; }

/* ---- STREAMLIT OVERRIDES ---- */
div[data-testid="stTabs"] button {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #f97316 !important;
    border-bottom: 2px solid #f97316 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f97316, #fbbf24) !important;
    color: #0a0e1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    padding: 10px 20px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button:disabled {
    background: var(--border) !important;
    color: var(--muted) !important;
    opacity: 0.5 !important;
}
.stTextInput > div > input,
.stNumberInput > div > input,
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}
.stAlert {
    border-radius: 10px !important;
}
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 14px !important;
}
</style>
""", unsafe_allow_html=True)


# ==============================================
# INISIALISASI SESSION STATE
# ==============================================

if 'kasir_list' not in st.session_state:
    st.session_state.kasir_list = {
        1: KasirQueue(1, "Kasir 1 — Budi",   tipe="reguler"),
        2: KasirQueue(2, "Kasir 2 — Sari",   tipe="reguler"),
        3: KasirQueue(3, "Kasir 3 — Rudi",   tipe="reguler"),
        4: KasirQueue(4, "Express — Dewi",   tipe="express"),
        5: KasirQueue(5, "Express — Anto",   tipe="express"),
    }

if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []

if 'nomor' not in st.session_state:
    st.session_state.nomor = 1

if 'total_transaksi' not in st.session_state:
    st.session_state.total_transaksi = 0

if 'pelanggan_selesai' not in st.session_state:
    st.session_state.pelanggan_selesai = []


def add_log(tipe, pesan):
    st.session_state.riwayat.append({
        "tipe": tipe,
        "pesan": pesan,
        "waktu": datetime.now().strftime("%H:%M:%S")
    })


# ==============================================
# HERO HEADER
# ==============================================

st.markdown("""
<div class="hero-header">
    <p class="hero-title">🛒 SuperMart Queue System</p>
    <p class="hero-sub">Sistem Manajemen Antrian Kasir Supermarket — Struktur Data <strong>Queue (FIFO)</strong></p>
    <div class="live-badge"><span class="live-dot"></span> SISTEM AKTIF</div>
</div>
""", unsafe_allow_html=True)


# ==============================================
# GLOBAL METRICS
# ==============================================

total_antri  = sum(k.size()            for k in st.session_state.kasir_list.values())
total_layani = sum(k.total_dilayani    for k in st.session_state.kasir_list.values())
total_item   = sum(k.total_item()      for k in st.session_state.kasir_list.values())
total_pend   = sum(k.total_pendapatan  for k in st.session_state.kasir_list.values())
kasir_buka   = sum(1 for k in st.session_state.kasir_list.values() if k.status == "Buka")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👥 Antrian Aktif",    total_antri,  "orang")
col2.metric("✅ Total Dilayani",   total_layani, "orang")
col3.metric("📦 Item dalam Antrian", total_item, "item")
col4.metric("💰 Est. Pendapatan",  f"Rp {total_pend:,.0f}")
col5.metric("🏪 Kasir Buka",       kasir_buka,   "kasir")

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================
# TABS
# ==============================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏪 Monitor Kasir",
    "➕ Tambah Pelanggan",
    "⚡ Auto-Assign",
    "✅ Layani & Proses",
    "🔁 Pindah Antrian",
    "📊 Analitik",
    "📋 Riwayat & Log",
])


# --------------------------------------------------
# TAB 1: MONITOR KASIR
# --------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">📡 Status Real-Time Semua Kasir</div>', unsafe_allow_html=True)

    cols = st.columns(len(st.session_state.kasir_list))
    for idx, (kid, kasir) in enumerate(st.session_state.kasir_list.items()):
        with cols[idx]:
            tipe_badge  = "badge-express" if kasir.tipe == "express" else "badge-reguler"
            tipe_label  = "⚡ Express"    if kasir.tipe == "express" else "🛒 Reguler"
            stat_badge  = f"badge-{kasir.status.lower()}"
            beban_color = {"Kosong": "#10b981", "Ringan": "#3b82f6", "Sedang": "#fbbf24", "Padat": "#ef4444"}
            beban       = kasir.beban()
            max_cap     = 5 if kasir.tipe == "express" else 10
            pct         = min(100, int(kasir.size() / max_cap * 100))

            st.markdown(f"""
            <div class="kasir-card">
                <div class="kasir-header">
                    <div>
                        <div class="kasir-title">{kasir.nama_kasir}</div>
                        <span class="badge {tipe_badge}">{tipe_label}</span>
                        &nbsp;<span class="badge {stat_badge}">{kasir.status}</span>
                    </div>
                </div>
                <div class="kasir-stats">
                    <div class="stat-mini"><span>Antrian</span><strong>{kasir.size()} orang</strong></div>
                    <div class="stat-mini"><span>Total Item</span><strong>{kasir.total_item()}</strong></div>
                    <div class="stat-mini"><span>Est. Tunggu</span><strong>~{kasir.estimasi_menit()} mnt</strong></div>
                    <div class="stat-mini"><span>Dilayani</span><strong>{kasir.total_dilayani}</strong></div>
                </div>
                <div style="font-size:0.72rem;color:var(--muted);margin-bottom:4px;">
                    Kepadatan: <strong style="color:{beban_color[beban]}">{beban}</strong> ({pct}%)
                </div>
                <div class="progress-bar-wrap">
                    <div class="progress-bar-fill" style="width:{pct}%"></div>
                </div>
                <div class="antrian-wrapper">
            """, unsafe_allow_html=True)

            if kasir.is_empty():
                st.markdown('<div class="empty-state">✨ Antrian Kosong</div>', unsafe_allow_html=True)
            else:
                for i, p in enumerate(kasir.daftar()[:5]):
                    css = "first" if i == 0 else ""
                    icon = "▶" if i == 0 else f"#{i+1}"
                    st.markdown(f"""
                    <div class="antrian-item {css}">
                        <div>
                            <div class="antrian-nama">{icon} {p.nama}</div>
                            <div class="antrian-info">🛍 {p.jumlah_item} item · {p.metode_bayar} · ⏱ {p.lama_menunggu()}</div>
                        </div>
                        <div style="font-size:0.7rem;color:var(--muted)">{p.id}</div>
                    </div>
                    """, unsafe_allow_html=True)
                if kasir.size() > 5:
                    st.markdown(f'<div class="antrian-info" style="text-align:center;padding:6px">+{kasir.size()-5} lainnya...</div>', unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)


# --------------------------------------------------
# TAB 2: TAMBAH PELANGGAN MANUAL
# --------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">➕ Daftarkan Pelanggan ke Antrian</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        nama_p = st.text_input("👤 Nama Pelanggan", placeholder="Contoh: Ibu Rina", value=f"Pelanggan-{st.session_state.nomor:03d}")
        jml_item = st.number_input("📦 Jumlah Item Belanja", min_value=1, max_value=200, value=12)
        metode = st.selectbox("💳 Metode Pembayaran", ["💵 Tunai", "💳 Kartu Debit", "📱 QRIS", "💳 Kartu Kredit", "🏦 Transfer"])
    with c2:
        # Kategori otomatis
        kategori = "express" if jml_item <= 10 else "reguler"
        st.info(f"💡 Kategori: **{'⚡ Express (≤10 item)' if kategori == 'express' else '🛒 Reguler (>10 item)'}**")

        # Filter kasir berdasarkan kategori
        kasir_sesuai = {k: v for k, v in st.session_state.kasir_list.items()
                        if v.tipe == kategori and v.status == "Buka"}
        kasir_semua  = {k: v for k, v in st.session_state.kasir_list.items() if v.status == "Buka"}

        if kasir_sesuai:
            rekomendasi = min(kasir_sesuai, key=lambda k: kasir_sesuai[k].size())
        elif kasir_semua:
            rekomendasi = min(kasir_semua, key=lambda k: kasir_semua[k].size())
        else:
            rekomendasi = 1

        st.success(f"✅ Rekomendasi: **{st.session_state.kasir_list[rekomendasi].nama_kasir}** (antrian: {st.session_state.kasir_list[rekomendasi].size()} orang)")

        pilih_kasir = st.selectbox(
            "🏪 Pilih Kasir Tujuan",
            options=[k for k, v in st.session_state.kasir_list.items() if v.status == "Buka"],
            format_func=lambda k: f"{st.session_state.kasir_list[k].nama_kasir} ({st.session_state.kasir_list[k].size()} antrian)",
            index=0
        )

        # Validasi express
        if st.session_state.kasir_list[pilih_kasir].tipe == "express" and jml_item > 10:
            st.warning("⚠️ Kasir Express hanya untuk ≤10 item!")

    if st.button("🛒 Masukkan ke Antrian (ENQUEUE)", type="primary", use_container_width=True):
        kasir_tujuan = st.session_state.kasir_list[pilih_kasir]
        if kasir_tujuan.tipe == "express" and jml_item > 10:
            st.error("❌ Tidak bisa! Kasir Express hanya untuk pelanggan ≤10 item.")
        elif nama_p.strip() == "":
            st.warning("⚠️ Nama pelanggan tidak boleh kosong!")
        else:
            p = Pelanggan(nama_p.strip(), jml_item, metode, kategori)
            kasir_tujuan.enqueue(p)
            st.session_state.nomor += 1
            add_log("enqueue", f"'{p.nama}' ({jml_item} item, {metode}) → {kasir_tujuan.nama_kasir} [ID: {p.id}]")
            st.success(f"✅ **{p.nama}** berhasil masuk ke **{kasir_tujuan.nama_kasir}**! Nomor antrian: **{p.id}**")
            st.rerun()


# --------------------------------------------------
# TAB 3: AUTO-ASSIGN BATCH
# --------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">⚡ Auto-Assign & Simulasi</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🤖 Generate Pelanggan Otomatis")
        jumlah_generate = st.slider("Jumlah pelanggan yang akan digenerate:", 1, 20, 5)
        nama_prefix = st.text_input("Prefix nama:", value="Customer")

        if st.button("⚡ Generate & Auto-Assign Sekarang", use_container_width=True):
            nama_pool = ["Andi", "Budi", "Citra", "Dian", "Eko", "Fani", "Gilang", "Hana",
                         "Ivan", "Julia", "Kevin", "Lina", "Maya", "Nino", "Ola", "Pandu"]
            metode_pool = ["💵 Tunai", "💳 Kartu Debit", "📱 QRIS", "💳 Kartu Kredit"]

            for _ in range(jumlah_generate):
                nm  = f"{nama_prefix}-{random.choice(nama_pool)}-{random.randint(10,99)}"
                itm = random.randint(1, 25)
                met = random.choice(metode_pool)
                kat = "express" if itm <= 10 else "reguler"

                # Cari kasir terbaik
                kasir_cocok = {k: v for k, v in st.session_state.kasir_list.items()
                               if v.tipe == kat and v.status == "Buka"}
                if not kasir_cocok:
                    kasir_cocok = {k: v for k, v in st.session_state.kasir_list.items() if v.status == "Buka"}
                if kasir_cocok:
                    tujuan = st.session_state.kasir_list[min(kasir_cocok, key=lambda k: kasir_cocok[k].size())]
                    p = Pelanggan(nm, itm, met, kat)
                    tujuan.enqueue(p)
                    add_log("enqueue", f"[AUTO] '{nm}' ({itm} item) → {tujuan.nama_kasir}")
                    st.session_state.nomor += 1

            st.success(f"✅ {jumlah_generate} pelanggan berhasil digenerate & didistribusikan secara otomatis!")
            st.rerun()

    with c2:
        st.subheader("⚙️ Kelola Status Kasir")
        for kid, kasir in st.session_state.kasir_list.items():
            col_n, col_s = st.columns([2, 2])
            with col_n:
                st.write(f"**{kasir.nama_kasir}**")
            with col_s:
                status_baru = st.selectbox(
                    "", ["Buka", "Tutup", "Istirahat"],
                    index=["Buka", "Tutup", "Istirahat"].index(kasir.status),
                    key=f"status_{kid}"
                )
                if status_baru != kasir.status:
                    add_log("status", f"{kasir.nama_kasir}: {kasir.status} → {status_baru}")
                    kasir.status = status_baru
                    st.rerun()


# --------------------------------------------------
# TAB 4: LAYANI PELANGGAN
# --------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">✅ Proses Checkout Pelanggan</div>', unsafe_allow_html=True)

    # Layani satu kasir
    st.subheader("Layani Pelanggan (DEQUEUE)")
    cols = st.columns(len(st.session_state.kasir_list))
    for idx, (kid, kasir) in enumerate(st.session_state.kasir_list.items()):
        with cols[idx]:
            peek = kasir.peek()
            if peek:
                st.markdown(f"""
                <div class="antrian-item first" style="margin-bottom:8px;flex-direction:column;align-items:flex-start">
                    <div class="antrian-nama">▶ {peek.nama}</div>
                    <div class="antrian-info">🛍 {peek.jumlah_item} item · {peek.metode_bayar}</div>
                    <div class="antrian-info">⏱ Menunggu: {peek.lama_menunggu()}</div>
                    <div class="antrian-info">🎫 {peek.id}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state">Kosong</div>', unsafe_allow_html=True)

            if st.button(f"✅ Layani", key=f"dq_{kid}", disabled=kasir.is_empty() or kasir.status != "Buka", use_container_width=True):
                selesai, harga = kasir.dequeue()
                st.session_state.total_transaksi += harga
                st.session_state.pelanggan_selesai.append({
                    "nama": selesai.nama, "item": selesai.jumlah_item,
                    "kasir": kasir.nama_kasir, "metode": selesai.metode_bayar,
                    "harga": harga, "waktu": datetime.now().strftime("%H:%M:%S")
                })
                add_log("dequeue", f"'{selesai.nama}' selesai checkout di {kasir.nama_kasir} — Est. Rp {harga:,.0f}")
                st.success(f"✅ **{selesai.nama}** selesai! Est. transaksi: **Rp {harga:,.0f}**")
                st.rerun()

    st.divider()

    # Layani semua kasir sekaligus
    st.subheader("⚡ Layani Semua Kasir Sekaligus")
    if st.button("✅✅ LAYANI SEMUA KASIR (BATCH DEQUEUE)", use_container_width=True):
        count = 0
        for kasir in st.session_state.kasir_list.values():
            if not kasir.is_empty() and kasir.status == "Buka":
                selesai, harga = kasir.dequeue()
                st.session_state.total_transaksi += harga
                add_log("dequeue", f"[BATCH] '{selesai.nama}' → {kasir.nama_kasir}")
                count += 1
        if count > 0:
            st.success(f"✅ {count} pelanggan berhasil dilayani sekaligus!")
            st.rerun()
        else:
            st.info("Semua antrian kosong atau kasir tutup.")

    st.divider()

    # Cari pelanggan by ID
    st.subheader("🔍 Cari Pelanggan by Nomor Tiket (PEEK)")
    cari_id = st.text_input("Masukkan ID Tiket (contoh: TKT-1234):", placeholder="TKT-XXXX")
    if st.button("🔍 Cari Tiket"):
        ditemukan = False
        for kasir in st.session_state.kasir_list.values():
            for pos, p in enumerate(kasir.daftar()):
                if p.id.upper() == cari_id.strip().upper():
                    st.success(f"🎫 Ditemukan! **{p.nama}** — Antrian ke-**{pos+1}** di **{kasir.nama_kasir}**")
                    st.info(f"📦 Item: {p.jumlah_item} | 💳 {p.metode_bayar} | ⏱ Menunggu: {p.lama_menunggu()}")
                    ditemukan = True
                    break
        if not ditemukan and cari_id:
            st.error(f"❌ Tiket **{cari_id}** tidak ditemukan dalam sistem.")


# --------------------------------------------------
# TAB 5: PINDAH ANTRIAN
# --------------------------------------------------
with tab5:
    st.markdown('<div class="section-title">🔁 Pindah Antrian Antar Kasir</div>', unsafe_allow_html=True)
    st.info("Fitur ini memindahkan pelanggan paling depan dari satu kasir ke kasir lain.")

    c1, c2, c3 = st.columns(3)
    with c1:
        kasir_asal = st.selectbox(
            "Dari Kasir:",
            options=list(st.session_state.kasir_list.keys()),
            format_func=lambda k: f"{st.session_state.kasir_list[k].nama_kasir} ({st.session_state.kasir_list[k].size()} orang)",
            key="asal"
        )
    with c2:
        kasir_tujuan_pindah = st.selectbox(
            "Ke Kasir:",
            options=[k for k in st.session_state.kasir_list.keys() if k != kasir_asal],
            format_func=lambda k: f"{st.session_state.kasir_list[k].nama_kasir} ({st.session_state.kasir_list[k].size()} orang)",
            key="tujuan_pindah"
        )
    with c3:
        st.write("")
        st.write("")
        if st.button("🔁 Pindahkan Pelanggan Depan", use_container_width=True):
            asal   = st.session_state.kasir_list[kasir_asal]
            tujuan = st.session_state.kasir_list[kasir_tujuan_pindah]
            if asal.is_empty():
                st.error("❌ Antrian kasir asal kosong!")
            elif tujuan.tipe == "express" and asal.peek().jumlah_item > 10:
                st.error("❌ Tidak bisa pindah! Kasir Express hanya untuk ≤10 item.")
            else:
                p = asal.antrian.popleft()
                tujuan.enqueue(p)
                add_log("status", f"[PINDAH] '{p.nama}' dari {asal.nama_kasir} → {tujuan.nama_kasir}")
                st.success(f"✅ **{p.nama}** berhasil dipindahkan ke **{tujuan.nama_kasir}**!")
                st.rerun()

    st.divider()
    st.subheader("⚖️ Seimbangkan Antrian Otomatis")
    st.write("Memindahkan pelanggan dari kasir terpadat ke kasir yang paling sepi secara otomatis.")
    if st.button("⚖️ Auto-Balance Semua Kasir", use_container_width=True):
        # Cari kasir terpadat dan tersepi (tipe sama)
        moved = 0
        for _ in range(5):  # Maksimal 5 perpindahan
            reguler = {k: v for k, v in st.session_state.kasir_list.items() if v.tipe == "reguler" and v.status == "Buka"}
            if len(reguler) >= 2:
                terpadat = max(reguler, key=lambda k: reguler[k].size())
                tersepi  = min(reguler, key=lambda k: reguler[k].size())
                if reguler[terpadat].size() - reguler[tersepi].size() > 2:
                    p = reguler[terpadat].antrian.popleft()
                    reguler[tersepi].enqueue(p)
                    moved += 1
        if moved > 0:
            st.success(f"✅ {moved} pelanggan berhasil dipindahkan untuk menyeimbangkan antrian!")
            st.rerun()
        else:
            st.info("Antrian sudah seimbang, tidak perlu perpindahan.")


# --------------------------------------------------
# TAB 6: ANALITIK
# --------------------------------------------------
with tab6:
    st.markdown('<div class="section-title">📊 Dashboard Analitik</div>', unsafe_allow_html=True)

    # Per-kasir stats
    st.subheader("📈 Perbandingan Performa Kasir")
    data_kasir = []
    for kasir in st.session_state.kasir_list.values():
        data_kasir.append({
            "Kasir": kasir.nama_kasir,
            "Antrian": kasir.size(),
            "Dilayani": kasir.total_dilayani,
            "Pendapatan (Rp)": kasir.total_pendapatan,
            "Avg Waktu (detik)": kasir.avg_waktu_layanan(),
            "Status": kasir.status,
            "Tipe": kasir.tipe.capitalize()
        })

    import pandas as pd
    df = pd.DataFrame(data_kasir)
    st.dataframe(df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Antrian per Kasir")
        st.bar_chart({k.nama_kasir: k.size() for k in st.session_state.kasir_list.values()})
    with c2:
        st.subheader("✅ Total Dilayani per Kasir")
        st.bar_chart({k.nama_kasir: k.total_dilayani for k in st.session_state.kasir_list.values()})

    st.subheader("🧾 Riwayat Transaksi Selesai (10 Terakhir)")
    if st.session_state.pelanggan_selesai:
        df_selesai = pd.DataFrame(st.session_state.pelanggan_selesai[-10:])
        df_selesai["harga"] = df_selesai["harga"].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(df_selesai, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada transaksi selesai.")


# --------------------------------------------------
# TAB 7: RIWAYAT & LOG
# --------------------------------------------------
with tab7:
    st.markdown('<div class="section-title">📋 Log Aktivitas Sistem</div>', unsafe_allow_html=True)

    icon_map = {"enqueue": "🟢", "dequeue": "🟠", "status": "🔵", "reset": "🔴"}

    filter_tipe = st.selectbox("Filter:", ["Semua", "enqueue", "dequeue", "status", "reset"])

    logs = st.session_state.riwayat if filter_tipe == "Semua" else [l for l in st.session_state.riwayat if l["tipe"] == filter_tipe]

    if logs:
        for log in reversed(logs[-50:]):
            icon = icon_map.get(log["tipe"], "⚪")
            st.markdown(f"""
            <div class="log-item {log['tipe']}">
                <span class="log-time">{log['waktu']}</span>
                {icon} {log['pesan']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada log aktivitas.")

    if st.button("🗑️ Hapus Semua Log"):
        st.session_state.riwayat = []
        st.rerun()


# ==============================================
# SIDEBAR: INFO & RESET
# ==============================================

with st.sidebar:
    st.markdown("## 🛒 SuperMart")
    st.markdown("**Sistem Manajemen Antrian**")
    st.markdown("---")
    st.markdown("### 📚 Info Struktur Data")
    st.markdown("""
- **Queue (FIFO)**: Pelanggan pertama masuk → pertama dilayani
- **Enqueue**: Tambah ke belakang antrian
- **Dequeue**: Ambil dari depan antrian
- **Peek**: Lihat depan tanpa mengambil
- **Express**: ≤10 item
- **Reguler**: >10 item
    """)

    st.markdown("---")
    st.markdown("### ⚙️ Tambah Kasir Baru")
    nama_kasir_baru = st.text_input("Nama Kasir:", placeholder="Kasir 6 — Nama")
    tipe_kasir_baru = st.selectbox("Tipe:", ["reguler", "express"])
    if st.button("➕ Tambah Kasir", use_container_width=True):
        if nama_kasir_baru.strip():
            new_id = max(st.session_state.kasir_list.keys()) + 1
            st.session_state.kasir_list[new_id] = KasirQueue(new_id, nama_kasir_baru.strip(), tipe_kasir_baru)
            add_log("status", f"Kasir baru ditambahkan: {nama_kasir_baru}")
            st.success(f"✅ {nama_kasir_baru} ditambahkan!")
            st.rerun()

    st.markdown("---")
    st.markdown(f"**🕒 Waktu:** {datetime.now().strftime('%H:%M:%S')}")
    st.markdown(f"**📅 Tanggal:** {datetime.now().strftime('%d %B %Y')}")
    st.markdown("---")

    if st.button("🔄 Reset Sistem", use_container_width=True):
        st.session_state.kasir_list = {
            1: KasirQueue(1, "Kasir 1 — Budi",  tipe="reguler"),
            2: KasirQueue(2, "Kasir 2 — Sari",  tipe="reguler"),
            3: KasirQueue(3, "Kasir 3 — Rudi",  tipe="reguler"),
            4: KasirQueue(4, "Express — Dewi",  tipe="express"),
            5: KasirQueue(5, "Express — Anto",  tipe="express"),
        }
        st.session_state.riwayat = []
        st.session_state.nomor = 1
        st.session_state.total_transaksi = 0
        st.session_state.pelanggan_selesai = []
        add_log("reset", "Sistem direset ke kondisi awal")
        st.success("✅ Sistem direset!")
        st.rerun()

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

    queue.reset_antrian()

    st.success("Semua antrian berhasil direset!")
