# 1. ANALISIS SPEEDUP SKALA PADA MULTIPROCESSING

import os

# Membatasi jumlah thread agar tidak terlalu membebani resource
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import multiprocessing as mp
import time
import matplotlib.pyplot as plt

# FUNGSI MENGHITUNG BILANGAN PRIMA
def hitung_prima(n):
    jumlah_prima = 0

    for angka in range(2, n + 1):
        prima = True

        for i in range(2, int(angka ** 0.5) + 1):
            if angka % i == 0:
                prima = False
                break

        if prima:
            jumlah_prima += 1

    return jumlah_prima

# PROGRAM UTAMA
def main():

    n = 80000

    jumlah_worker = [1, 2, 4, 8]

    waktu = []

    # Pengujian waktu eksekusi
    for worker in jumlah_worker:

        ctx = mp.get_context("spawn")

        mulai = time.perf_counter()

        with ctx.Pool(processes=worker) as pool:

            hasil = pool.map(
                hitung_prima,
                [n] * worker
            )

        selesai = time.perf_counter()

        waktu_eksekusi = selesai - mulai

        waktu.append(waktu_eksekusi)

        print(
            f"Worker = {worker}, "
            f"Waktu = {waktu_eksekusi:.4f} detik"
        )


    # PERHITUNGAN SPEEDUP
    waktu_worker_1 = waktu[0]

    speedup = []

    for t in waktu:
        speedup.append(waktu_worker_1 / t)

    # PERHITUNGAN HUKUM AMDAHL
    P = 1

    speedup_amdahl = []

    for worker in jumlah_worker:

        nilai = 1 / ((1 - P) + (P / worker))

        speedup_amdahl.append(nilai)

    # MENAMPILKAN HASIL SPEEDUP
    print("\nHasil Speedup:")

    for worker, sp in zip(jumlah_worker, speedup):

        print(
            f"Worker = {worker}, "
            f"Speedup = {sp:.2f}x"
        )

    # MENAMPILKAN SPEEDUP IDEAL
    print("\nSpeedup Ideal Hukum Amdahl:")

    for worker, sp in zip(jumlah_worker, speedup_amdahl):

        print(
            f"Worker = {worker}, "
            f"Speedup Ideal = {sp:.2f}x"
        )


    # PLOT SPEEDUP
    plt.figure(figsize=(8, 5))

    plt.plot(
        jumlah_worker,
        speedup,
        marker="o",
        label="Speedup Aktual"
    )

    plt.plot(
        jumlah_worker,
        speedup_amdahl,
        marker="o",
        linestyle="--",
        label="Hukum Amdahl (Ideal)"
    )

    plt.xlabel("Jumlah Worker")
    plt.ylabel("Speedup")

    plt.title(
        "Perbandingan Speedup Aktual dan Hukum Amdahl"
    )

    plt.xticks(jumlah_worker)

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()


# ANALISIS
# Berdasarkan hasil pengujian, dilakukan perbandingan waktu
# eksekusi menggunakan 1, 2, 4, dan 8 worker. Speedup dihitung
# dengan membandingkan waktu eksekusi menggunakan 1 worker
# dengan waktu eksekusi pada setiap jumlah worker.
#
# Secara teori, semakin banyak worker yang digunakan maka
# proses dapat berjalan lebih cepat sehingga speedup meningkat.
# Berdasarkan Hukum Amdahl, speedup ideal untuk 1, 2, 4, dan
# 8 worker adalah 1x, 2x, 4x, dan 8x.
#
# Namun, hasil aktual dapat berbeda dari hasil ideal karena
# adanya overhead multiprocessing, seperti pembuatan proses
# dan pengaturan worker. Penggunaan worker yang terlalu banyak
# juga dapat membebani resource komputer sehingga penambahan
# worker tidak selalu membuat program menjadi lebih cepat.

# KESIMPULAN
# Berdasarkan pengujian, penggunaan multiprocessing dengan
# jumlah worker yang lebih banyak tidak selalu meningkatkan
# kecepatan program. Speedup aktual dapat berbeda dari speedup
# ideal Hukum Amdahl karena adanya overhead multiprocessing
# dan keterbatasan resource komputer.

if __name__ == "__main__":
    main()