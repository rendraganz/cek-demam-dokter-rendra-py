# Kode indikator gejala
kode_gejala = [
    "G1", "G2", "G3", "G4", "G5", "G6", "G7",
    "G8", "G9", "G10", "G11", "G12", "G13", "G14"
]

# Nama gejala sesuai urutan kode G1-G14
gejala = [
    "Demam",
    "Mual",
    "Muntah",
    "Lemes",
    "Mencret",
    "Kejang",
    "Tenggorokan sakit",
    "Bintik merah",
    "Mimisan",
    "Nyeri sendi",
    "Pusing",
    "Leukosit",
    "Hematokrit",
    "Trombosit"
]

# Data kasus lama (nilai biner 1 dan 0)
nama_kasus = ["DBD 1", "DBD 2", "DBD 3", "DBD 4"]

case_lama = [
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
]

# Data kasus baru (nilai biner 1 dan 0)
case_baru = [
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0]
]

# menghitung dot product antara kasus baru dan kasus lama
dot_product = []
for i in case_baru:
    for j in case_lama:
        dot = 0
        for idx in range(len(i)):
            dot += i[idx] * j[idx]
        dot_product = dot_product + [dot]
        print(f"DBD {case_lama.index(j) + 1} x P5: {dot}")

# panjang vektor kasus lama (DBD 1 - DBD 4)
panjang_lama = []
for j in case_lama:
    kuadrat = 0
    for angka in j:
        kuadrat += angka ** 2
    panjang = kuadrat ** 0.5
    panjang_lama = panjang_lama + [panjang]
    print(f"Panjang DBD {case_lama.index(j) + 1}: {panjang:.3f}")

# panjang vektor kasus baru (P5)
panjang_baru = []
for i in case_baru:
    kuadrat = 0
    for angka in i:
        kuadrat += angka ** 2
    panjang = kuadrat ** 0.5
    panjang_baru = panjang_baru + [panjang]
    print(f"Panjang P5: {panjang:.3f}")

    # print(f"{panjang_lama[2]:.3f}") 

# menghitung cosine similarity
for i in range(len(dot_product)):
    cosine_similarity = dot_product[i] / (panjang_lama[i] * panjang_baru[0])
    persentase = cosine_similarity * 100
    print(f"Cosine Similarity DBD {i + 1} x P5: {cosine_similarity:.3f} ({persentase:.2f}%)")
