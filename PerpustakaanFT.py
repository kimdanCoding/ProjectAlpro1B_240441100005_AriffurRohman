# Database
user_accounts = {}
admin_accounts = {"admin": "admin123"}  # akun petugas awal (username: admin, password: admin123)
books = [
    {"title": "Harry Poter the philosopher stone", "author": "Jk Rowling", "id": "01", "stock": 5},
    {"title": "Harry Poter the prisioner of azkaban", "author": "Jk Rowling", "id": "02", "stock": 3},
    {"title": "Harry Poter goblet of fire", "author": "Jk Rowling", "id": "03", "stock": 2},
]  # Daftar buku default
borrow_records = []

# Fungsi untuk membuat akun pengguna
def create_account():
    username = input("Masukkan username baru: ")
    if username in user_accounts:
        print("Username sudah ada! Coba username lain.")
        return
    password = input("Masukkan password: ")
    nim = input("Masukkan NIM: ")
    user_accounts[username] = {"password": password, "nim": nim}
    print("Akun pengguna berhasil dibuat!\n")

# Fungsi untuk membuat akun petugas
def create_admin_account():
    username = input("Masukkan username petugas baru: ")
    if username in admin_accounts:
        print("Username petugas sudah ada! Coba username lain.")
        return
    password = input("Masukkan password petugas: ")
    admin_accounts[username] = password
    print("Akun petugas berhasil dibuat!\n")

# Fungsi login
def login():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    if username in user_accounts and user_accounts[username]["password"] == password:
        print("Login berhasil sebagai pengguna!")
        user_menu(username)
    elif username in admin_accounts and admin_accounts[username] == password:
        print("Login berhasil sebagai petugas!")
        admin_menu()
    else:
        print("Username atau password salah!\n")

# Fungsi melihat daftar buku yang tersedia
def view_books():
    if not books:
        print("Tidak ada buku yang tersedia.\n")
    else:
        print("Daftar Buku:")
        for i, book in enumerate(books, start=1):
            print(f"{i}. {book['title']} - {book['author']} (ID: {book['id']}, Stok: {book['stock']})")
    print()

# Fungsi untuk meminjam buku
def borrow_book(username):
    view_books()
    book_id = input("Masukkan ID buku yang ingin dipinjam: ")
    selected_book = next((book for book in books if book["id"] == book_id), None)

    if selected_book:
        if selected_book["stock"] > 0:
            nim = user_accounts[username]["nim"]
            borrow_date = input("Masukkan tanggal pinjam (YYYY-MM-DD): ")
            return_date = input("Masukkan tanggal kembali (YYYY-MM-DD): ")
            record = {
                "username": username,
                "nim": nim,
                "book_id": book_id,
                "borrow_date": borrow_date,
                "return_date": return_date
            }
            borrow_records.append(record)
            selected_book["stock"] -= 1  # Mengurangi stok buku yang dipinjam
            print(f"Buku berhasil dipinjam sampai {return_date}. Ingat untuk mengembalikan tepat waktu!")
            print(f"Stok buku setelah peminjaman: {selected_book['stock']}\n")
        else:
            print("Stok buku tidak tersedia.\n")
    else:
        print("Buku tidak ditemukan.\n")

# Fungsi untuk mengembalikan buku dan menghitung denda
def return_book(username):
    user_borrows = [record for record in borrow_records if record["username"] == username]
    if not user_borrows:
        print("Tidak ada buku yang dipinjam.\n")
        return
    
    for i, record in enumerate(user_borrows, start=1):
        print(f"{i}. ID Buku: {record['book_id']}, Tanggal Pinjam: {record['borrow_date']}, Tanggal Kembali: {record['return_date']}")
    
    try:
        choice = int(input("Pilih nomor buku yang ingin dikembalikan: ")) - 1
        if choice < 0 or choice >= len(user_borrows):
            print("Pilihan tidak valid.\n")
            return
        borrow_record = user_borrows[choice]
        
        # Memasukkan tanggal pengembalian aktual
        actual_return_date = input("Masukkan tanggal pengembalian (YYYY-MM-DD): ")

        # Menghitung selisih tanggal
        borrow_year, borrow_month, borrow_day = map(int, borrow_record["return_date"].split("-"))
        return_year, return_month, return_day = map(int, actual_return_date.split("-"))

        # Menghitung denda jika terlambat
        delay_days = (return_year - borrow_year) * 365 + (return_month - borrow_month) * 30 + (return_day - borrow_day)
        
        if delay_days > 0:
            fine = delay_days * 10000
            print(f"Terlambat {delay_days} hari. Anda dikenakan denda sebesar Rp {fine}.")
        else:
            print("Buku dikembalikan tepat waktu. Tidak ada denda.")
        
        # Menghapus record peminjaman setelah buku dikembalikan
        borrow_records.remove(borrow_record)
        
        # Menambah stok buku setelah dikembalikan
        for book in books:
            if book["id"] == borrow_record["book_id"]:
                book["stock"] += 1
                print(f"Stok buku setelah pengembalian: {book['stock']}\n")
                break
        
        print("Buku berhasil dikembalikan!\n")
    except ValueError:
        print("Input tidak valid. Pastikan format tanggalnya benar (YYYY-MM-DD).\n")

# Fungsi menu pengguna
def user_menu(username):
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Lihat Daftar Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. Keluar")
        choice = input("Pilih menu: ")
        
        if choice == "1":
            view_books()
        elif choice == "2":
            borrow_book(username)
        elif choice == "3":
            return_book(username)
        elif choice == "4":
            break
        else:
            print("Pilihan tidak valid.\n")

# Fungsi menambah buku oleh petugas
def add_book():
    title = input("Masukkan judul buku: ")
    author = input("Masukkan pengarang: ")
    book_id = input("Masukkan ID buku: ")
    stock = int(input("Masukkan stok buku: "))
    books.append({"title": title, "author": author, "id": book_id, "stock": stock})
    print("Buku berhasil ditambahkan!\n")

# Fungsi menghapus buku oleh petugas
def remove_book():
    book_id = input("Masukkan ID buku yang ingin dihapus: ")
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            print("Buku berhasil dihapus!\n")
            return
    print("Buku tidak ditemukan.\n")

# Fungsi melihat daftar peminjam
def view_borrow_records():
    if not borrow_records:
        print("Tidak ada peminjaman saat ini.\n")
    else:
        print("Daftar Peminjam:")
        for record in borrow_records:
            print(f"Username: {record['username']}, NIM: {record['nim']}, ID Buku: {record['book_id']}, Tanggal Pinjam: {record['borrow_date']}, Tanggal Kembali: {record['return_date']}")
    print()

# Fungsi menu petugas
def admin_menu():
    while True:
        print("\n=== Menu Petugas ===")
        print("1. Lihat Daftar Buku")
        print("2. Tambah Buku")
        print("3. Hapus Buku")
        print("4. Lihat Daftar Peminjam")
        print("5. Keluar")
        choice = input("Pilih menu: ")
        
        if choice == "1":
            view_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            remove_book()
        elif choice == "4":
            view_borrow_records()
        elif choice == "5":
            break
        else:
            print("Pilihan tidak valid.\n")

# Fungsi utama
while True:
    print("\n=== Perpustakaan Fakultas Teknik ===")
    print("1. Buat Akun Pengguna")
    print("2. Buat Akun Petugas")
    print("3. Login")
    print("4. Keluar")
    main_choice = input("Pilih menu: ")
    
    if main_choice == "1":
        create_account()
    elif main_choice == "2":
        create_admin_account()
    elif main_choice == "3":
        login()
    elif main_choice == "4":
        print("Terima kasih telah menggunakan sistem perpustakaan!")
        break
    else:
        print("Pilihan tidak valid.\n")