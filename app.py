from pathlib import Path
import json
import streamlit as st

st.set_page_config(
    page_title="DokterRendra - Spesialis Cek Demam",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════
#  DATA  (sama persis dengan cosine-dbd.py)
# ══════════════════════════════════════════════════
kode_gejala = [
    "G1", "G2", "G3", "G4", "G5", "G6", "G7",
    "G8", "G9", "G10", "G11", "G12", "G13", "G14"
]
gejala = [
    "Demam", "Mual", "Muntah", "Lemes", "Mencret", "Kejang",
    "Tenggorokan sakit", "Bintik merah", "Mimisan", "Nyeri sendi",
    "Pusing", "Leukosit", "Hematokrit", "Trombosit"
]
nama_kasus  = ["DBD 1", "DBD 2", "DBD 3", "DBD 4"]
grade_dbd   = [
    "Demam Berdarah Grade I",
    "Demam Berdarah Grade II",
    "Demam Berdarah Grade III",
    "Demam Berdarah Grade IV"
]
case_lama_awal = [
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
]
preset_p5 = [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0]


def salin_list_2d(matriks):
    return [[e for e in b] for b in matriks]


# ══════════════════════════════════════════════════
#  KALKULASI  (logika persis cosine-dbd.py)
# ══════════════════════════════════════════════════
def hitung_cbr(vektor_baru, case_lama, daftar_nama, daftar_grade):
    cb = [vektor_baru]

    # Dot product antara kasus baru dan kasus lama
    dot_product = []
    for i in cb:
        for j in case_lama:
            dot = 0
            for idx in range(len(i)):
                dot += i[idx] * j[idx]
            dot_product = dot_product + [dot]

    # Panjang vektor kasus lama
    panjang_lama = []
    for j in case_lama:
        kuadrat = 0
        for angka in j:
            kuadrat += angka ** 2
        panjang_lama = panjang_lama + [kuadrat ** 0.5]

    # Panjang vektor kasus baru
    kuadrat = 0
    for angka in cb[0]:
        kuadrat += angka ** 2
    panjang_baru = kuadrat ** 0.5

    # Cosine similarity
    hasil_cosine = []
    persen_list  = []
    for i in range(len(dot_product)):
        penyebut = panjang_lama[i] * panjang_baru
        cs  = 0.0 if penyebut == 0 else dot_product[i] / penyebut
        pct = cs * 100
        hasil_cosine = hasil_cosine + [cs]
        persen_list  = persen_list  + [pct]

    # Cari indeks tertinggi
    idx_max = 0
    for i in range(1, len(hasil_cosine)):
        if hasil_cosine[i] > hasil_cosine[idx_max]:
            idx_max = i

    # Ranking (bubble sort descending)
    urutan = list(range(len(hasil_cosine)))
    for i in range(len(urutan)):
        for j in range(i + 1, len(urutan)):
            if hasil_cosine[urutan[j]] > hasil_cosine[urutan[i]]:
                urutan[i], urutan[j] = urutan[j], urutan[i]

    return {
        "dot_product":     dot_product,
        "panjang_lama":    panjang_lama,
        "panjang_baru":    panjang_baru,
        "hasil_cosine":    hasil_cosine,
        "persen_list":     persen_list,
        "idx_tertinggi":   idx_max,
        "urutan_idx":      urutan,
        "kasus_tertinggi": daftar_nama[idx_max],
        "grade_tertinggi": daftar_grade[idx_max],
        "nilai_tertinggi": hasil_cosine[idx_max],
        "persen_tertinggi":persen_list[idx_max],
    }



# ══════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════
ss = st.session_state
ss.setdefault("menu_aktif", "Dashboard")
ss.setdefault("kasus_nama", list(nama_kasus))
ss.setdefault("kasus_grade", list(grade_dbd))
ss.setdefault("kasus_vektor", salin_list_2d(case_lama_awal))
ss.setdefault("riwayat", [])
ss.setdefault("hasil_terakhir", None)
for _i in range(len(kode_gejala)):
    ss.setdefault(f"chk_{_i}", False)


# ══════════════════════════════════════════════════
#  LOAD CSS
# ══════════════════════════════════════════════════
css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )


def judul(teks, sub):
    return (f'<div class="section-intro"><h1>{teks}</h1>'
            f'<p class="muted">{sub}</p></div>')


# ══════════════════════════════════════════════════
#  HEADER + NAVIGASI (tab horizontal, tanpa sidebar)
# ══════════════════════════════════════════════════
menu_keys = ["Dashboard", "Diagnosis", "Riwayat Diagnosis", "Basis Kasus", "Tentang"]

st.markdown("""
<a class="skip-link" href="#konten">Lewati ke konten utama</a>
<header class="topbar">
  <div class="brand">
    <div class="brand-mark" aria-hidden="true">D</div>
    <div><strong>DokterRendra</strong><span>Spesialis Cek Demam</span></div>
  </div>
  <div class="top-actions"><span class="status-dot" aria-hidden="true"></span>Prototype aktif</div>
</header>
""", unsafe_allow_html=True)

with st.container(key="nav"):
    for _col, _m in zip(st.columns(len(menu_keys)), menu_keys):
        with _col:
            if st.button(_m, key=f"nav_{_m}", type="primary" if _m == ss.menu_aktif else "secondary"):
                if _m != ss.menu_aktif:
                    ss.menu_aktif = _m
                    st.rerun()

st.markdown(
    f'<div id="konten" tabindex="-1"><span class="sr-only">Halaman aktif: {ss.menu_aktif}</span></div>',
    unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  VIEW: DASHBOARD
# ══════════════════════════════════════════════════
if ss.menu_aktif == "Dashboard":

    st.markdown("""
<section class="hero-banner" aria-labelledby="h-hero">
  <div class="hero-text">
    <span class="hero-badge">Clinical decision support</span>
    <h1 id="h-hero">Cek kemiripan kasus demam berdarah dengan CBR</h1>
    <p>Bandingkan gejala pasien dengan kasus referensi memakai cosine similarity, lalu tinjau dan simpan hasilnya sebagai pengetahuan baru.</p>
    <ul class="hero-chips"><li>Cosine similarity</li><li>4 tahap CBR</li><li>Data ilustrasi, bukan data klinis</li></ul>
  </div>
</section>
""", unsafe_allow_html=True)

    with st.container(key="aksi-dash"):
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Mulai diagnosis", type="primary", use_container_width=True):
                ss.menu_aktif = "Diagnosis"
                st.rerun()
        with d2:
            if st.button("Lihat basis kasus", use_container_width=True):
                ss.menu_aktif = "Basis Kasus"
                st.rerun()

    n_kasus, n_riwayat = len(ss.kasus_nama), len(ss.riwayat)
    st.markdown(f"""
<div class="stats-grid">
  <article class="stat-card">
    <div class="stat-icon blue" aria-hidden="true">▤</div>
    <div><span class="stat-label">Kasus referensi</span><strong>{n_kasus}</strong><small>Di basis kasus saat ini</small></div>
  </article>
  <article class="stat-card">
    <div class="stat-icon violet" aria-hidden="true">⌕</div>
    <div><span class="stat-label">Diagnosis tersimpan</span><strong>{n_riwayat}</strong><small>Hanya di sesi ini</small></div>
  </article>
  <article class="stat-card">
    <div class="stat-icon teal" aria-hidden="true">✓</div>
    <div><span class="stat-label">Siklus CBR</span><strong>4 tahap</strong><small>Retrieve, Reuse, Revise, Retain</small></div>
  </article>
</div>
""", unsafe_allow_html=True)

    chips_html = ""
    for idx in range(n_kasus):
        jml = sum(ss.kasus_vektor[idx])
        chips_html += f"""<div class="case-chip"><div class="case-tag" aria-hidden="true">P{idx+1}</div><div><strong>{ss.kasus_nama[idx]}</strong><small>{ss.kasus_grade[idx]}</small></div><span class="count">{jml} gejala</span></div>"""

    st.markdown(f"""
<div class="content-grid">
  <section class="panel" aria-labelledby="h-cbr">
    <div class="panel-head">
      <div><h2 id="h-cbr">Alur Case-Based Reasoning</h2><p class="muted">Cara sistem mencari kasus yang mirip</p></div>
      <span class="pill">CBR</span>
    </div>
    <ol class="cbr-flow">
      <li class="flow-step"><span class="flow-num">1</span><div><strong>Retrieve</strong><p>Bandingkan gejala kasus baru dengan kasus referensi memakai cosine similarity.</p></div></li>
      <li class="flow-step"><span class="flow-num">2</span><div><strong>Reuse</strong><p>Pakai label kasus dengan kemiripan tertinggi sebagai hasil simulasi.</p></div></li>
      <li class="flow-step"><span class="flow-num">3</span><div><strong>Revise</strong><p>Periksa dan koreksi hasil secara manual untuk demonstrasi akademik.</p></div></li>
      <li class="flow-step"><span class="flow-num">4</span><div><strong>Retain</strong><p>Simpan kasus yang sudah ditinjau ke basis kasus sesi ini.</p></div></li>
    </ol>
  </section>
  <section class="panel" aria-labelledby="h-basis">
    <div class="panel-head">
      <div><h2 id="h-basis">Basis kasus</h2><p class="muted">Label yang dipakai sebagai contoh</p></div>
    </div>
    <div class="case-overview">{chips_html}</div>
    <div class="divider"></div>
    <p class="helper">Kasus DBD 1–DBD 4 adalah data ilustrasi untuk demonstrasi metode, bukan data klinis tervalidasi.</p>
  </section>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<section class="panel formula-panel" aria-labelledby="h-rumus">
  <div><h2 id="h-rumus">Metode perhitungan</h2><p class="muted">Cosine similarity mengukur kemiripan dua vektor gejala biner.</p></div>
  <div class="formula" role="img" aria-label="sim(x, y) sama dengan x titik y dibagi norma x kali norma y">
    <span aria-hidden="true">sim(x,y) =</span>
    <span class="fraction" aria-hidden="true"><span>x &middot; y</span><span>&#x2016;x&#x2016; &times; &#x2016;y&#x2016;</span></span>
  </div>
</section>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  VIEW: DIAGNOSIS
# ══════════════════════════════════════════════════
elif ss.menu_aktif == "Diagnosis":

    st.markdown(judul("Simulasi diagnosis",
                      "Isi profil contoh dan pilih gejala untuk membandingkan kasus."),
                unsafe_allow_html=True)

    with st.container(key="aksi"):
        tb1, tb2 = st.columns(2)
        with tb1:
            if st.button("Isi contoh P5", use_container_width=True):
                for i, v in enumerate(preset_p5):
                    ss[f"chk_{i}"] = (v == 1)
                st.rerun()
        with tb2:
            if st.button("Reset gejala", use_container_width=True):
                for i in range(len(kode_gejala)):
                    ss[f"chk_{i}"] = False
                st.rerun()

    with st.form("form_diagnosis_dbd"):
        st.markdown("""
<div class="form-section-title">
  <span class="section-number" aria-hidden="true">1</span>
  <div><h2>Informasi subjek</h2><p class="muted">Data hanya tersimpan di sesi ini.</p></div>
</div>
""", unsafe_allow_html=True)

        f1, f2, f3 = st.columns([1.5, 0.7, 1])
        with f1:
            nama_pasien = st.text_input("Nama pasien", placeholder="Contoh: Budi Santoso")
        with f2:
            umur_pasien = st.number_input("Umur (tahun)", min_value=0, max_value=120, value=21, step=1)
        with f3:
            gender_pasien = st.selectbox(
                "Jenis kelamin", ["Tidak disebutkan", "Laki-laki", "Perempuan"]
            )

        st.markdown("""
<div class="form-section-title symptoms-title">
  <span class="section-number" aria-hidden="true">2</span>
  <div><h2>Pilih gejala</h2><p class="muted">Centang gejala yang ada. Semua gejala berbobot sama.</p></div>
</div>
""", unsafe_allow_html=True)

        vektor_baru, gejala_aktif = [], []
        with st.container(key="gejala"):
            for idx in range(len(kode_gejala)):
                aktif = st.checkbox(f"**{kode_gejala[idx]}** · {gejala[idx]}", key=f"chk_{idx}")
                vektor_baru.append(1 if aktif else 0)
                if aktif:
                    gejala_aktif.append(f"{kode_gejala[idx]} ({gejala[idx]})")

        submit_btn = st.form_submit_button("Hitung kemiripan", type="primary", use_container_width=True)

    if submit_btn:
        if not any(vektor_baru):
            st.warning("Pilih minimal satu gejala sebelum menghitung kemiripan.")
        else:
            hasil = hitung_cbr(vektor_baru, ss.kasus_vektor, ss.kasus_nama, ss.kasus_grade)
            catatan = {
                "nama": nama_pasien.strip() or "Pasien Tanpa Nama",
                "umur": int(umur_pasien),
                "gender": gender_pasien,
                "vektor_baru": vektor_baru,
                "gejala_aktif": gejala_aktif,
                "hasil": hasil,
            }
            ss.hasil_terakhir = catatan
            ss.riwayat = [catatan] + ss.riwayat

    if ss.hasil_terakhir is not None:
        d = ss.hasil_terakhir
        res = d["hasil"]

        rows_html = ""
        for rank, i in enumerate(res["urutan_idx"]):
            bar_w = max(0, min(100, round(res["persen_list"][i])))
            best = "best-row" if rank == 0 else ""
            badge = '<span class="badge">Termirip</span>' if rank == 0 else ""
            rows_html += f"""<tr class="{best}"><td><strong>#{rank+1}</strong></td><td><strong>{ss.kasus_nama[i]}</strong>{badge}</td><td>{ss.kasus_grade[i]}</td><td class="opt">{res['dot_product'][i]}</td><td class="opt">{res['panjang_lama'][i]:.3f}</td><td class="opt">{res['panjang_baru']:.3f}</td><td><span class="score-track" aria-hidden="true"><span class="score-fill" style="width:{bar_w}%"></span></span>{res['hasil_cosine'][i]:.3f}</td><td>{res['persen_list'][i]:.2f}%</td></tr>"""

        gejala_str = ", ".join(d["gejala_aktif"]) if d["gejala_aktif"] else "—"

        st.markdown(f"""
<section class="result-card" aria-live="polite" aria-labelledby="h-hasil">
  <div class="result-top">
    <div>
      <div class="result-kicker">Hasil retrieve</div>
      <h2 id="h-hasil">{res['kasus_tertinggi']} &mdash; {res['grade_tertinggi']}</h2>
      <p class="muted"><strong>{d['nama']}</strong> ({d['umur']} tahun, {d['gender']})<br>Gejala: {gejala_str}</p>
    </div>
    <div class="result-score">{res['nilai_tertinggi']:.3f}<small>{res['persen_tertinggi']:.2f}% kemiripan</small></div>
  </div>
  <div class="table-wrap" role="region" aria-label="Peringkat kemiripan, bisa digulir" tabindex="0">
    <table>
      <caption class="sr-only">Peringkat kemiripan kasus baru terhadap kasus referensi</caption>
      <thead><tr>
        <th scope="col">Rank</th><th scope="col">Kasus</th><th scope="col">Grade DBD</th>
        <th scope="col" class="opt">Dot product</th><th scope="col" class="opt">&#x2016;Lama&#x2016;</th><th scope="col" class="opt">&#x2016;Baru&#x2016;</th>
        <th scope="col">Similarity</th><th scope="col">Persen</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</section>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  VIEW: RIWAYAT DIAGNOSIS
# ══════════════════════════════════════════════════
elif ss.menu_aktif == "Riwayat Diagnosis":

    with st.container(key="hero"):
        r1, r2 = st.columns([3, 1])
        with r1:
            st.markdown(judul("Riwayat diagnosis", "Data tersimpan di sesi ini, bukan di server."),
                        unsafe_allow_html=True)
        with r2:
            if ss.riwayat:
                json_data = json.dumps(
                    [
                        {
                            "nama": r["nama"],
                            "umur": r["umur"],
                            "gender": r["gender"],
                            "vektor_baru": r["vektor_baru"],
                            "kasus_tertinggi": r["hasil"]["kasus_tertinggi"],
                            "grade_tertinggi": r["hasil"]["grade_tertinggi"],
                            "cosine_tertinggi": round(r["hasil"]["nilai_tertinggi"], 3),
                            "persentase_tertinggi": round(r["hasil"]["persen_tertinggi"], 2),
                        }
                        for r in ss.riwayat
                    ],
                    indent=2, ensure_ascii=False
                )
                st.download_button(
                    "Ekspor JSON", data=json_data,
                    file_name="riwayat-diagnosis-dbd.json",
                    mime="application/json", use_container_width=True
                )

    if not ss.riwayat:
        st.markdown("""
<div class="panel"><div class="empty-state">
  <strong>Belum ada riwayat</strong>
  Jalankan simulasi di tab Diagnosis, hasilnya muncul di sini.
</div></div>
""", unsafe_allow_html=True)
    else:
        items_html = ""
        for idx, r in enumerate(ss.riwayat):
            hs = r["hasil"]
            gejala_str = ", ".join(r["gejala_aktif"]) if r["gejala_aktif"] else "—"
            items_html += f"""<li class="history-item"><div class="case-tag" aria-hidden="true">P{idx+1}</div><div class="history-info"><strong>{r['nama']} ({r['umur']} th, {r['gender']})</strong><small>{hs['kasus_tertinggi']} &mdash; {hs['grade_tertinggi']}<br>Gejala: {gejala_str}</small></div><div class="history-score">{hs['nilai_tertinggi']:.3f} <span class="tag-neutral">{hs['persen_tertinggi']:.1f}%</span></div></li>"""

        st.markdown(f'<div class="panel"><ul class="history-list">{items_html}</ul></div>',
                    unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  VIEW: BASIS KASUS
# ══════════════════════════════════════════════════
elif ss.menu_aktif == "Basis Kasus":

    with st.container(key="hero"):
        bk1, bk2 = st.columns([3, 1])
        with bk1:
            st.markdown(judul("Basis kasus",
                              "Kasus awal dan kasus yang ditambahkan lewat Retain."),
                        unsafe_allow_html=True)
        with bk2:
            if st.button("Pulihkan kasus awal", use_container_width=True):
                ss.kasus_nama = list(nama_kasus)
                ss.kasus_grade = list(grade_dbd)
                ss.kasus_vektor = salin_list_2d(case_lama_awal)
                st.rerun()

    if ss.get("pesan"):
        st.success(ss.pop("pesan"))

    header_th = '<th scope="col">Kasus</th><th scope="col">Grade DBD</th>'
    for kg in kode_gejala:
        header_th += f'<th scope="col" class="num">{kg}</th>'

    rows_html = ""
    for idx in range(len(ss.kasus_nama)):
        cells = f'<td><strong>{ss.kasus_nama[idx]}</strong></td><td>{ss.kasus_grade[idx]}</td>'
        for v in ss.kasus_vektor[idx]:
            cells += f'<td class="num {"on" if v == 1 else "off"}">{v}</td>'
        rows_html += f"<tr>{cells}</tr>"

    legenda = " · ".join(f"<strong>{k}</strong> {g}" for k, g in zip(kode_gejala, gejala))
    st.markdown(f"""
<div class="panel">
  <details class="legend"><summary>Keterangan kode gejala</summary><p>{legenda}</p></details>
  <div class="table-wrap" role="region" aria-label="Matriks basis kasus, bisa digulir" tabindex="0" style="margin-top:0">
    <table class="matrix">
      <caption class="sr-only">Matriks kasus referensi: 1 berarti gejala ada, 0 berarti tidak ada</caption>
      <thead><tr>{header_th}</tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</div>
""", unsafe_allow_html=True)

    head_retain = """
<div class="panel-head">
  <div><h2>Revise &amp; Retain</h2><p class="muted">Tinjau hasil terakhir, koreksi label, lalu simpan sebagai kasus baru.</p></div>
  <span class="pill">Manual review</span>
</div>"""

    if ss.hasil_terakhir is None:
        st.markdown(f"""
<div class="panel">{head_retain}
  <div class="empty-state">Jalankan simulasi di tab Diagnosis dulu untuk meninjau dan menyimpan kasus.</div>
</div>
""", unsafe_allow_html=True)
    else:
        terakhir = ss.hasil_terakhir
        opsi_grade = list(grade_dbd)
        default_grade = terakhir["hasil"]["grade_tertinggi"]
        idx_def = opsi_grade.index(default_grade) if default_grade in opsi_grade else 0
        gejala_str = ", ".join(terakhir["gejala_aktif"]) if terakhir["gejala_aktif"] else "—"

        st.markdown(f"""
<div class="panel">{head_retain}
  <div class="review-box" style="margin-bottom:0">
    <strong>{terakhir['nama']}</strong> ({terakhir['umur']} th, {terakhir['gender']})<br>
    Hasil retrieve: <strong>{terakhir['hasil']['kasus_tertinggi']}</strong> &mdash; {terakhir['hasil']['grade_tertinggi']} ({terakhir['hasil']['persen_tertinggi']:.2f}%)<br>
    Gejala: {gejala_str}
  </div>
</div>
""", unsafe_allow_html=True)

        grade_koreksi = st.selectbox("Koreksi atau tetapkan Grade DBD (Revise)", opsi_grade, index=idx_def)
        if st.button("Simpan ke basis kasus (Retain)", type="primary"):
            nomor_baru = len(ss.kasus_nama) + 1
            ss.kasus_nama = ss.kasus_nama + [f"DBD {nomor_baru}"]
            ss.kasus_grade = ss.kasus_grade + [grade_koreksi]
            ss.kasus_vektor = ss.kasus_vektor + [list(terakhir["vektor_baru"])]
            # pesan disimpan dulu karena st.rerun() menghapus elemen yang tampil
            ss.pesan = f"Kasus baru tersimpan sebagai **DBD {nomor_baru}** ({grade_koreksi})."
            st.rerun()


elif ss.menu_aktif == "Tentang":

    st.markdown("""
<section class="profile-hero" aria-labelledby="h-profil">
  <div class="avatar" aria-hidden="true">MR</div>
  <div class="profile-main">
    <span class="hero-badge">Pengembang</span>
    <h1 id="h-profil">Muhammad Rendra Irawan</h1>
    <p>Mahasiswa kelas 3D TRPL, pembuat aplikasi DokterRendra.</p>
  </div>
</section>
<dl class="profile-grid">
  <div class="profile-item"><dt>Nama lengkap</dt><dd>Muhammad Rendra Irawan</dd></div>
  <div class="profile-item"><dt>NIM</dt><dd class="num">362458302036</dd></div>
  <div class="profile-item"><dt>Kelas</dt><dd>3D TRPL</dd></div>
  <div class="profile-item"><dt>Tugas</dt><dd>Sistem Pendukung Keputusan</dd></div>
</dl>
<section class="panel" aria-labelledby="h-app">
  <h2 id="h-app">Tentang aplikasi</h2>
  <p class="muted">DokterRendra adalah prototype sistem pendukung keputusan untuk simulasi pencarian kasus demam berdarah yang paling mirip. Aplikasi ini dibuat untuk tujuan pembelajaran dan bukan alat diagnosis klinis.</p>
  <ul class="tech-chips"><li>Python</li><li>Streamlit</li><li>Case-Based Reasoning</li><li>Cosine similarity</li></ul>
</section>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════
st.markdown(
    '<footer class="app-footer">copyright rendraganz - tugas Sistem Pendukung Keputusan</footer>',
    unsafe_allow_html=True
)
