# 4. REFLEKSI: MANAGER() VS VALUE/ARRAY

# Saya akan memilih Manager() jika membuat program yang membutuhkan
# beberapa proses untuk berbagi data dengan struktur yang lebih
# kompleks, misalnya list atau dict. Manager lebih mudah digunakan
# karena data dapat diakses dan dimodifikasi oleh beberapa proses
# tanpa harus mengatur shared memory secara langsung. Namun,
# kemudahannya memiliki konsekuensi berupa performa yang lebih
# rendah karena komunikasi dengan Manager membutuhkan proses
# tambahan.
#
# Sebaliknya, saya akan memilih Value/Array jika data yang dibagikan
# sederhana dan membutuhkan performa yang lebih tinggi, misalnya
# menyimpan angka atau kumpulan nilai dengan ukuran tertentu.
# Value/Array lebih cepat karena menggunakan shared memory secara
# langsung, tetapi penggunaannya lebih terbatas dan membutuhkan
# perhatian terhadap sinkronisasi seperti Lock.
#
# Jadi, Manager lebih cocok ketika kemudahan penggunaan menjadi
# prioritas, sedangkan Value/Array lebih cocok ketika performa
# menjadi prioritas.