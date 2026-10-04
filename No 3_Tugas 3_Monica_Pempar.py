# 3. PRODUCER-CONSUMER ANTAR-PROSES
# CPU-BOUND: MULTIPROCESSING VS THREADING
import multiprocessing as mp
import threading
import queue
import time

# KONSTANTA
JUMLAH_PRODUCER = 2
JUMLAH_CONSUMER = 2

# Jumlah tugas yang dibuat oleh setiap producer
JUMLAH_TUGAS_PER_PRODUCER = 20

# Batas perhitungan untuk tugas CPU-bound
BATAS_PRIMA_AWAL = 20000

# FUNGSI CPU-BOUND
def hitung_prima(n):
    """
    Menghitung jumlah bilangan prima dari 2 sampai n.
    Perhitungan ini digunakan sebagai beban CPU-bound.
    """

    jumlah = 0
    for angka in range(2, n + 1):
        prima = True
        for pembagi in range(2, int(angka ** 0.5) + 1):
            if angka % pembagi == 0:
                prima = False
                break
        if prima:
            jumlah += 1
    return jumlah

# PRODUCER
def producer(producer_id, task_queue):
    """
    Producer menghasilkan tugas berupa angka.
    Tugas dimasukkan ke dalam Queue untuk diproses consumer.
    """
    for i in range(JUMLAH_TUGAS_PER_PRODUCER):
        # Membuat tugas yang sama untuk pengujian
        # multiprocessing dan threading
        nilai = (
            BATAS_PRIMA_AWAL
            + (i * 100)
            + (producer_id * 50)
        )
        task_queue.put(nilai)

# CONSUMER
def consumer(task_queue, result_queue):
    """
    Consumer mengambil tugas dari Queue dan melakukan
    perhitungan CPU-bound.
    """
    jumlah_tugas = 0
    total_hasil = 0
    while True:
        tugas = task_queue.get()
        # None digunakan sebagai tanda bahwa producer
        # sudah selesai dan consumer harus berhenti
        if tugas is None:
            break
        hasil = hitung_prima(tugas)
        total_hasil += hasil
        jumlah_tugas += 1

    # Mengirim hasil consumer
    result_queue.put(
        (jumlah_tugas, total_hasil)
    )

# VERSI 1
# MULTIPROCESSING
def jalankan_multiprocessing():
    print("VERSI 1: MULTIPROCESSING")

    # Context spawn untuk Windows
    ctx = mp.get_context("spawn")

    # Queue antar-proses
    task_queue = ctx.Queue()

    # Queue untuk mengirim hasil consumer
    result_queue = ctx.Queue()
    producers = []
    consumers = []
    mulai = time.perf_counter()

    # Membuat consumer
    for _ in range(JUMLAH_CONSUMER):
        p = ctx.Process(
            target=consumer,
            args=(task_queue, result_queue)
        )
        consumers.append(p)
        p.start()

    # Membuat producer
    for i in range(JUMLAH_PRODUCER):
        p = ctx.Process(
            target=producer,
            args=(i, task_queue)
        )
        producers.append(p)
        p.start()

    # Menunggu semua producer selesai
    for p in producers:
        p.join()

    # Mengirim tanda berhenti untuk setiap consumer
    for _ in range(JUMLAH_CONSUMER):
        task_queue.put(None)

    # Menunggu semua consumer selesai
    for p in consumers:
        p.join()
    selesai = time.perf_counter()
    waktu = selesai - mulai

    # Mengambil hasil dari consumer
    jumlah_tugas = 0
    total_hasil = 0

    for _ in range(JUMLAH_CONSUMER):
        jumlah, hasil = result_queue.get()
        jumlah_tugas += jumlah
        total_hasil += hasil

    print(f"Jumlah tugas diproses : {jumlah_tugas}")
    print(f"Total hasil           : {total_hasil}")
    print(f"Waktu eksekusi        : {waktu:.4f} detik")
    return waktu

# VERSI 2
# THREADING
def jalankan_threading():
    print("VERSI 2: THREADING")

    # Queue untuk komunikasi antar-thread
    task_queue = queue.Queue()

    # Queue untuk hasil consumer
    result_queue = queue.Queue()
    producers = []
    consumers = []
    mulai = time.perf_counter()

    # Membuat consumer
    for _ in range(JUMLAH_CONSUMER):
        t = threading.Thread(
            target=consumer,
            args=(task_queue, result_queue)
        )
        consumers.append(t)
        t.start()

    # Membuat producer
    for i in range(JUMLAH_PRODUCER):
        t = threading.Thread(
            target=producer,
            args=(i, task_queue)
        )
        producers.append(t)
        t.start()

    # Menunggu semua producer selesai
    for t in producers:
        t.join()

    # Mengirim tanda berhenti untuk setiap consumer
    for _ in range(JUMLAH_CONSUMER):
        task_queue.put(None)

    # Menunggu semua consumer selesai
    for t in consumers:
        t.join()
    selesai = time.perf_counter()
    waktu = selesai - mulai

    # Mengambil hasil dari consumer
    jumlah_tugas = 0
    total_hasil = 0
    for _ in range(JUMLAH_CONSUMER):
        jumlah, hasil = result_queue.get()
        jumlah_tugas += jumlah
        total_hasil += hasil

    print(f"Jumlah tugas diproses : {jumlah_tugas}")
    print(f"Total hasil           : {total_hasil}")
    print(f"Waktu eksekusi        : {waktu:.4f} detik")
    return waktu

def main():
    print("PRODUCER-CONSUMER ANTAR-PROSES")
    print("CPU-BOUND")
    print(f"\nJumlah producer              : {JUMLAH_PRODUCER}")
    print(f"Jumlah consumer              : {JUMLAH_CONSUMER}")
    print(
        f"Jumlah tugas per producer    : "
        f"{JUMLAH_TUGAS_PER_PRODUCER}"
    )
    print(
        f"Total tugas                  : "
        f"{JUMLAH_PRODUCER * JUMLAH_TUGAS_PER_PRODUCER}"
    )

    # Menjalankan multiprocessing
    waktu_multiprocessing = jalankan_multiprocessing()

    # Menjalankan threading
    waktu_threading = jalankan_threading()

    # Perbandingan
    print("PERBANDINGAN PERFORMA")

    print(
        f"Multiprocessing : "
        f"{waktu_multiprocessing:.4f} detik"
    )
    print(
        f"Threading       : "
        f"{waktu_threading:.4f} detik"
    )

    # Menghitung speedup multiprocessing terhadap threading
    speedup = waktu_threading / waktu_multiprocessing

    print(
        f"\nSpeedup multiprocessing terhadap threading "
        f": {speedup:.2f}x"
    )
    if waktu_multiprocessing < waktu_threading:
        print(
            "Hasil: multiprocessing lebih cepat "
            "daripada threading."
        )
    elif waktu_threading < waktu_multiprocessing:
        print(
            "Hasil: threading lebih cepat "
            "daripada multiprocessing."
        )
    else:
        print(
            "Hasil: kedua metode memiliki "
            "waktu yang sama."
        )

# ANALISIS
# Program menggunakan pola producer-consumer. Producer bertugas
# menghasilkan tugas dan memasukkannya ke dalam Queue, sedangkan
# consumer mengambil tugas dari Queue dan melakukan perhitungan.
#
# Beban yang digunakan adalah perhitungan jumlah bilangan prima.
# Perhitungan tersebut membutuhkan penggunaan CPU sehingga
# termasuk CPU-bound, bukan I/O-bound.
#
# Pada versi multiprocessing, producer dan consumer dijalankan
# sebagai proses yang berbeda menggunakan multiprocessing.Process
# dan komunikasi dilakukan menggunakan multiprocessing.Queue.
# Setiap proses memiliki ruang memori sendiri sehingga proses CPU
# dapat berjalan secara paralel pada beberapa core CPU.
#
# Pada versi threading, producer dan consumer dijalankan sebagai
# thread menggunakan threading.Thread dan queue.Queue.
# Karena tugas yang diberikan bersifat CPU-bound, eksekusi thread
# dipengaruhi oleh Global Interpreter Lock (GIL) pada Python.
# Akibatnya, beberapa thread Python tidak dapat menjalankan kode
# Python CPU-bound secara paralel pada beberapa core seperti
# multiprocessing.
#
# Oleh karena itu, untuk tugas CPU-bound, multiprocessing biasanya
# memberikan performa yang lebih baik dibandingkan threading.
# Namun, hasil waktu aktual tetap bergantung pada spesifikasi
# komputer dan kondisi sistem saat program dijalankan.

# KESIMPULAN
# Berdasarkan perbandingan, multiprocessing lebih sesuai untuk
# pekerjaan CPU-bound karena setiap proses dapat berjalan pada
# core CPU yang berbeda. Sementara itu, threading lebih cocok
# untuk pekerjaan yang banyak menunggu I/O seperti membaca file,
# jaringan, atau menunggu respons.
#
# Pada tugas producer-consumer ini, perbedaan performa antara
# multiprocessing dan threading dapat diamati dari waktu eksekusi
# yang dihasilkan program. Metode dengan waktu eksekusi lebih kecil
# merupakan metode yang lebih cepat untuk beban CPU-bound yang
# digunakan pada pengujian.

if __name__ == "__main__":
    main()