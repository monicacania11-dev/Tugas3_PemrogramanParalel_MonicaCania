# 2. SHARED MEMORY VS MESSAGE PASSING

import os

# Membatasi thread agar multiprocessing tidak membebani resource
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import multiprocessing as mp
import random
import time

# KONSTANTA
JUMLAH_PROSES = 4
JUMLAH_ANGKA = 1_000_000

# VERSI 1: MESSAGE PASSING MENGGUNAKAN QUEUE
def proses_queue(queue, seed):

    # Membuat generator angka acak dengan seed berbeda
    random.seed(seed)

    # Menghitung subtotal 1 juta angka acak
    subtotal = 0.0

    for _ in range(JUMLAH_ANGKA):
        subtotal += random.random()

    # Mengirim subtotal ke proses utama melalui Queue
    queue.put(subtotal)

def jalankan_queue():

    # Menggunakan spawn karena program dijalankan di Windows
    ctx = mp.get_context("spawn")

    # Membuat Queue untuk komunikasi antarproses
    queue = ctx.Queue()

    proses = []

    mulai = time.perf_counter()

    # Membuat 4 proses
    for i in range(JUMLAH_PROSES):

        p = ctx.Process(
            target=proses_queue,
            args=(queue, 100 + i)
        )

        proses.append(p)
        p.start()

    # Menunggu semua proses selesai
    for p in proses:
        p.join()

    # Proses utama menerima subtotal dari setiap proses
    total = 0.0

    for _ in range(JUMLAH_PROSES):
        total += queue.get()

    selesai = time.perf_counter()

    waktu = selesai - mulai

    return total, waktu

# VERSI 2: SHARED MEMORY MENGGUNAKAN VALUE + LOCK
def proses_shared_value(nilai, lock, seed):

    # Membuat generator angka acak dengan seed berbeda
    random.seed(seed)

    # Menghitung subtotal 1 juta angka acak
    subtotal = 0.0

    for _ in range(JUMLAH_ANGKA):
        subtotal += random.random()

    # Mengubah shared Value dengan Lock
    with lock:
        nilai.value += subtotal

def jalankan_shared_value():

    # Menggunakan spawn karena program dijalankan di Windows
    ctx = mp.get_context("spawn")

    # Shared Value untuk menyimpan total
    nilai = ctx.Value("d", 0.0)

    # Lock untuk mencegah race condition
    lock = ctx.Lock()

    proses = []

    mulai = time.perf_counter()

    # Membuat 4 proses
    for i in range(JUMLAH_PROSES):

        p = ctx.Process(
            target=proses_shared_value,
            args=(nilai, lock, 100 + i)
        )

        proses.append(p)
        p.start()

    # Menunggu semua proses selesai
    for p in proses:
        p.join()

    selesai = time.perf_counter()

    waktu = selesai - mulai

    return nilai.value, waktu

def main():

    print("=" * 60)
    print("LATIHAN MANDIRI 2")
    print("SHARED MEMORY VS MESSAGE PASSING")
    print("=" * 60)

    print(f"\nJumlah proses       : {JUMLAH_PROSES}")
    print(f"Angka per proses   : {JUMLAH_ANGKA:,}")
    print(f"Total angka        : {JUMLAH_PROSES * JUMLAH_ANGKA:,}")

    # PENGUJIAN QUEUE
    print("\n--- Versi 1: Queue (Message Passing) ---")

    total_queue, waktu_queue = jalankan_queue()

    print(f"Total hasil         : {total_queue:.6f}")
    print(f"Waktu eksekusi      : {waktu_queue:.4f} detik")

    # PENGUJIAN VALUE + LOCK
    print("\n--- Versi 2: Value + Lock (Shared Memory) ---")

    total_shared, waktu_shared = jalankan_shared_value()

    print(f"Total hasil         : {total_shared:.6f}")
    print(f"Waktu eksekusi      : {waktu_shared:.4f} detik")

    # PERBANDINGAN
    print("\n--- Perbandingan Waktu Eksekusi ---")

    print(
        f"Queue       : {waktu_queue:.4f} detik"
    )

    print(
        f"Value+Lock  : {waktu_shared:.4f} detik"
    )

    if waktu_queue < waktu_shared:

        print(
            "\nQueue memiliki waktu eksekusi lebih cepat."
        )

    elif waktu_shared < waktu_queue:

        print(
            "\nValue + Lock memiliki waktu eksekusi lebih cepat."
        )

    else:

        print(
            "\nKedua metode memiliki waktu eksekusi yang sama."
        )

# ANALISIS
# Pada metode Queue, setiap proses menghitung subtotal dari
# 1 juta angka acak. Setelah selesai, subtotal dikirim ke proses
# utama melalui Queue. Proses utama kemudian mengambil subtotal
# dari Queue dan menjumlahkannya untuk mendapatkan total akhir.
#
# Pada metode Value + Lock, setiap proses juga menghitung subtotal
# dari 1 juta angka acak. Setelah selesai, subtotal ditambahkan
# langsung ke shared Value. Lock digunakan agar hanya satu proses
# yang mengubah shared Value pada satu waktu sehingga tidak terjadi
# race condition.
#
# Perbedaan waktu eksekusi dipengaruhi oleh mekanisme komunikasi
# dan sinkronisasi yang digunakan. Queue membutuhkan komunikasi
# antarproses untuk mengirim subtotal, sedangkan Value + Lock
# menggunakan memori bersama dan membutuhkan Lock ketika shared
# Value diperbarui.

# KESIMPULAN
# Queue menggunakan message passing sehingga data subtotal
# dikirim dari proses ke proses utama. Sementara itu, Value + Lock
# menggunakan shared memory sehingga proses dapat memperbarui
# nilai yang sama dengan perlindungan Lock.
#
# Berdasarkan hasil pengukuran waktu eksekusi, metode yang
# memiliki waktu lebih kecil merupakan metode yang lebih cepat
# pada komputer yang digunakan. Perbedaan hasil dapat terjadi
# karena overhead komunikasi Queue dan overhead sinkronisasi Lock.

if __name__ == "__main__":
    main()