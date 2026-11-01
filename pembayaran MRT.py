# Sistem Pembayaran MRT Jakarta
# WI1102 Berpikir Komputasional K-37
# Kelompok 6

# Konstanta Tarif
TARIF_DASAR = 2000
TARIF_PER_STASIUN = 1000
TARIF_MINIMUM = 3000
TARIF_MAKSIMUM = 14000
SALDO_MINIMUM = TARIF_MAKSIMUM  # saldo minimum untuk masuk = tarif maksimum

# Data Stasiun Array
daftar_stasiun = [
    "Stasiun Lebak Bulus Bank Syariah Indonesia",
    "Stasiun Fatmawati Indomaret",
    "Stasiun Cipete Raya",
    "Stasiun Haji Nawi",
    "Stasiun Blok A",
    "Stasiun Blok M BCA",
    "Stasiun ASEAN",
    "Stasiun Senayan Mastercard",
    "Stasiun Istora Mandiri",
    "Stasiun Bendungan Hilir",
    "Stasiun Setiabudi Astra",
    "Stasiun Dukuh Atas BNI",
    "Stasiun Bundaran HI Bank DKI",
]

# Data Kartu
daftar_id_kartu = []
daftar_saldo_kartu = []


# Sub Program Umum
""" Jadi awalnya user input angka raw contohnya "14000". lalu "return "Rp "" itu ngawalin format dengan Rp
    nah disini si f"{angka:,}" ngubah angka raw menjadi angka yang dibagi jadi 3. contohnya 14,000.
    terus fungsi replace itu menggantikan koma dengan titik. jadinya Rp + 14,000 + diubah ke . jadinya 14.000"""
    # Sumber https://www.datacamp.com/id/tutorial/python-f-string
def format_rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")

""" input_bilangan_bulat(pesan) terus meminta input sampai pengguna mengetik angka bulat ≥ 0. 
    .strip() membuang spasi, dan .isdigit() mengecek semua karakter adalah digit. Misalnya user ga sengaja ngetik " 14000 ".
    Nah karena ada .strip maka hasilnya akan menjadi "14000"
    Input kosong, huruf, desimal, atau negatif (ada tanda -) ditolak. Fungsi ini mengembalikan int. 
    Pakai while karena jumlah pengulangannya tidak diketahui."""
# sumber https://www.w3schools.com/python/default.asp
def input_bilangan_bulat(pesan):
    teks = input(pesan).strip()
    while not teks.isdigit():
        print("Input harus berupa angka bulat (tanpa titik/koma/huruf).")
        teks = input(pesan).strip()
    return int(teks)


def tampilkan_stasiun():
    #ini ngeprint daftar stasiun tapi penomoran dimulai dari 1, bukan dari 0. sehingga jadi 1 - 13
    print("Daftar stasiun:")
    for i in range(len(daftar_stasiun)):
        print(f"  {i + 1}. {daftar_stasiun[i]}")


def pilih_stasiun(pesan):
    """Ini fungsi pilih stasiun. kalo kurang dari 1 atau lebih dari len maka nomor st tdk valid.
    menggunakan (atau) karena bila ada salah satu kondisi terjadi, maka print nomor tdk valid akan terjadi"""
    tampilkan_stasiun()
    while True:
        nomor = input_bilangan_bulat(pesan)
        if nomor < 1 or nomor > len(daftar_stasiun):
            print("Nomor stasiun tidak valid.")
        else:
            return nomor - 1


# Sub Program Kartu & Saldo
def minta_id_kartu():
    """user input id kartu.(.strip) masih memiliki fungsi yang sama yaitu membuat input menghilangkan 
    hal yang tidak diperlukan. Menggunakan while bila isiny kosong maka harus ada input ID Kartu."""
    id_kartu = input("Masukkan ID kartu: ").strip()
    while id_kartu == "":
        id_kartu = input("ID kartu tidak boleh kosong. Masukkan ID kartu: ").strip()
    return id_kartu


def cari_kartu(id_kartu):
    """Ini mencari kartu. bila sudah terdaftar maka akan mengembalikan kartu.
    jika tidak, maka akan mengembalikan -1. -1 dipakai sebagai penanda tidak ada"""
    for i in range(len(daftar_id_kartu)):
        if daftar_id_kartu[i] == id_kartu:
            return i
    return -1


def ambil_posisi_kartu(id_kartu):
    """Disini mencari posisi kartu. Bila kartu baru, maka kartu akan didaftarkan terlebih dahulu dengan input saldo awal.
    Setelahnya, akan dimasukkan ke array kosong yang sudah disiapkan diatas dengan menggunakan append."""
    posisi = cari_kartu(id_kartu)
    if posisi == -1:
        saldo_awal = input_bilangan_bulat("Kartu baru. Masukkan saldo awal (Rp): ")
        daftar_id_kartu.append(id_kartu)
        daftar_saldo_kartu.append(saldo_awal)
        posisi = len(daftar_id_kartu) - 1
    return posisi


def top_up_saldo(posisi, boleh_batal):
    """Fungsi ini yaitu top up saldo. ada dua keadaan yaitu bila boleh batal dan tidak. Boleh batal bila topup dilakukan
    sebelum tap in kartu. Tidak boleh batal bila saldo kartu kurang ketika ingin keluar dari gerbang kereta akhir (tap out).
    ketika nominal 0 dan bukan kategori boleh batal (wajib topup), nominal harus lebih dari 0. jika 0 terus menerus yang terinput, maka
    akan terus berulang"""
    if boleh_batal:
        pesan = "Nominal top up (Rp), ketik 0 untuk batal: "
    else:
        pesan = "Nominal top up (Rp): "
    nominal = input_bilangan_bulat(pesan)
    while nominal == 0 and not boleh_batal:
        print("Nominal top up harus lebih dari 0.")
        nominal = input_bilangan_bulat(pesan)
    if nominal == 0:
        return False
    daftar_saldo_kartu[posisi] = daftar_saldo_kartu[posisi] + nominal
    print("Top up berhasil. Saldo sekarang :", format_rupiah(daftar_saldo_kartu[posisi]))
    return True


def pastikan_saldo_cukup(posisi, total_pembayaran):
    #Dipakai saat tap out yaitu selama saldo kurang dari tarif, wajib top up
    while daftar_saldo_kartu[posisi] < total_pembayaran:
        kurang = total_pembayaran - daftar_saldo_kartu[posisi]
        print(f"\nSaldo tidak cukup! Tarif {format_rupiah(total_pembayaran)}, "
              f"saldo {format_rupiah(daftar_saldo_kartu[posisi])}, "
              f"kurang {format_rupiah(kurang)}.")
        print("Gerbang keluar belum dapat dibuka. Silakan top up.")
        top_up_saldo(posisi, False)


# Hitung Tarif
def hitung_jumlah_stasiun(indeks_awal, indeks_akhir):
    #banyak stasiun yang ditempuh (selisih nomor urut stasiun)
    selisih = indeks_akhir - indeks_awal
    if selisih < 0:
        selisih = -selisih
    return selisih


def hitung_tarif_mentah(jumlah_stasiun):
    #Tarif dasar + tarif per stasiun
    return TARIF_DASAR + TARIF_PER_STASIUN * jumlah_stasiun


def terapkan_batas_tarif(tarif):
    #Pastikan tarif berada di antara tarif minimum dan maksimum
    if tarif < TARIF_MINIMUM:
        return TARIF_MINIMUM
    elif tarif > TARIF_MAKSIMUM:
        return TARIF_MAKSIMUM
    else:
        return tarif


# Sub Program Perjalanan
def tap_in():
    #Proses tap in. Mengembalikan (posisi_kartu, indeks_stasiun_awal), atau (-1, -1) jika tap in ditolak
    print("Tap In")
    posisi = ambil_posisi_kartu(minta_id_kartu())
    print("Saldo saat tap in :", format_rupiah(daftar_saldo_kartu[posisi]))

    # Saldo harus cukup untuk tarif maksimum. kalo kurang, tawarkan top up
    while daftar_saldo_kartu[posisi] < SALDO_MINIMUM:
        print(f"Saldo minimum untuk masuk adalah {format_rupiah(SALDO_MINIMUM)}.")
        if not top_up_saldo(posisi, True):
            print("Tap in ditolak. Silakan top up terlebih dahulu.")
            return -1, -1

    indeks_awal = pilih_stasiun("Pilih stasiun masuk (nomor): ")
    print(f"Tap in berhasil di {daftar_stasiun[indeks_awal]}. Selamat jalan!")
    return posisi, indeks_awal


def simulasi_potongan_perjalanan(posisi):
    #saldo kartu terpotong transaksi selama perjalanan
    pesan = ("Saldo terpotong transaksi lain selama perjalanan "
             "(Rp, ketik 0 jika tidak ada): ")
    potongan = input_bilangan_bulat(pesan)
    while potongan > daftar_saldo_kartu[posisi]:
        print("Potongan tidak boleh melebihi saldo kartu.")
        potongan = input_bilangan_bulat(pesan)
    daftar_saldo_kartu[posisi] = daftar_saldo_kartu[posisi] - potongan


def cetak_rincian_saldo(saldo_tap_in, potongan_lain, top_up_gerbang, total_pembayaran, saldo_akhir):
    #Cetak bagian saldo 
    """Disini ada yang baru yaitu :<18. Ini berfungsi sebagai label yang harus memiliki 18 karakter. Contohnya:
    Saldo saat tap in :
    Potongan lain     :
    Top up di gerbang :
    dst"""
    print(f"{'Saldo saat tap in':<18}: {format_rupiah(saldo_tap_in)}")
    if potongan_lain > 0:
        print(f"{'Potongan lain':<18}: - {format_rupiah(potongan_lain)}")
    if top_up_gerbang > 0:
        print(f"{'Top up di gerbang':<18}: + {format_rupiah(top_up_gerbang)}")
    print(f"{'Total pembayaran':<18}: {format_rupiah(total_pembayaran)}")
    print(f"{'Saldo akhir':<18}: {format_rupiah(saldo_akhir)}")
    print("-" * 60)


def tap_out(posisi, indeks_awal, saldo_tap_in):
    #Proses tap out:hitung tarif, pastikan saldo cukup, potong saldo, cetak struk
    print("\n Tap Out")
    indeks_akhir = pilih_stasiun("Pilih stasiun keluar (nomor): ")

    jumlah_stasiun = hitung_jumlah_stasiun(indeks_awal, indeks_akhir)
    tarif_mentah = hitung_tarif_mentah(jumlah_stasiun)
    total_pembayaran = terapkan_batas_tarif(tarif_mentah)

    saldo_sebelum_bayar = daftar_saldo_kartu[posisi]
    pastikan_saldo_cukup(posisi, total_pembayaran)
    top_up_gerbang = daftar_saldo_kartu[posisi] - saldo_sebelum_bayar
    potongan_lain = saldo_tap_in - saldo_sebelum_bayar
    saldo_akhir = daftar_saldo_kartu[posisi] - total_pembayaran
    daftar_saldo_kartu[posisi] = saldo_akhir

    print("STRUK PERJALANAN MRT JAKARTA (TARIF PER STASIUN)")
    print(f"{'ID kartu':<18}: {daftar_id_kartu[posisi]}")
    print(f"{'Stasiun awal':<18}: {daftar_stasiun[indeks_awal]}")
    print(f"{'Stasiun akhir':<18}: {daftar_stasiun[indeks_akhir]}")
    print(f"{'Stasiun ditempuh':<18}: {jumlah_stasiun}")
    print(f"{'Hitungan tarif':<18}: {format_rupiah(TARIF_DASAR)} + ({TARIF_PER_STASIUN} x {jumlah_stasiun})"
          f" = {format_rupiah(tarif_mentah)}")
    if tarif_mentah < TARIF_MINIMUM:
        print(f"{'Keterangan':<18}: di bawah tarif minimum, dikenakan {format_rupiah(TARIF_MINIMUM)}")
    elif tarif_mentah > TARIF_MAKSIMUM:
        print(f"{'Keterangan':<18}: di atas tarif maksimum, dikenakan {format_rupiah(TARIF_MAKSIMUM)}")
    cetak_rincian_saldo(saldo_tap_in, potongan_lain, top_up_gerbang, total_pembayaran, saldo_akhir)


def naik_mrt():
    #Satu perjalanan lengkap tap in, (di perjalanan), tap out
    posisi, indeks_awal = tap_in()
    if posisi != -1:
        saldo_tap_in = daftar_saldo_kartu[posisi]
        simulasi_potongan_perjalanan(posisi)
        tap_out(posisi, indeks_awal, saldo_tap_in)


def menu_top_up():
    #Menu top up saldo kartu di luar perjalanan
    print("\n=== TOP UP SALDO ===")
    posisi = ambil_posisi_kartu(minta_id_kartu())
    print("Saldo saat ini    :", format_rupiah(daftar_saldo_kartu[posisi]))
    top_up_saldo(posisi, True)


def menu_cek_saldo():
    #Menu cek saldo kartu
    print("\nCek Saldo")
    posisi = ambil_posisi_kartu(minta_id_kartu())
    print("Saldo kartu:", format_rupiah(daftar_saldo_kartu[posisi]))


# Program Utama
def main():
    print("\nSistem Pembayaran MRT Jakarta (Tarif per Stasiun)")
    pilihan = ""
    while pilihan != "0":
        print("MENU")
        print("  1. Naik MRT (tap in & tap out)")
        print("  2. Top up saldo kartu")
        print("  3. Cek saldo kartu")
        print("  0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            naik_mrt()
        elif pilihan == "2":
            menu_top_up()
        elif pilihan == "3":
            menu_cek_saldo()
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan MRT Jakarta.")
        else:
            print("Pilihan tidak valid.")


main()

"""Program ini dikerjakan dengan bantuan AI dengan prompt "dilarang memberikan program instan.
Sebaliknya, bertindaklah sebagai socratic tutor yang mengajukan pertanyaan penuntun demi memicu productive struggle
untuk program ini." sehingga saya dapat brainstorming dengan lancar dengan AI dan tetap mengerjakan program tanpa instan."""