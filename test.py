import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# ==========================================
# 1. MATERI: OOP
# ==========================================
class Laptop:
    def __init__(self, id_laptop, merk, tipe, ram, storage, harga, kategori):
        self.id = id_laptop
        self.merk = merk
        self.tipe = tipe
        self.ram = int(ram)
        self.storage = int(storage)
        self.harga = int(harga)
        self.kategori = kategori

class RekomendasiLaptopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Rekomendasi Laptop")
        self.root.geometry("750x650")
        
        self.bg_color = "#F4F6F9" 
        self.root.configure(bg=self.bg_color)
        self.selected_laptop_id = None

        # ==========================================
        # 2 & 6. MATERI: Array & Stack
        # ==========================================
        self.data_laptop = [] 
        self.stack_undo = [] 
        self.counter_id = 1 
        
        # Nama file penyimpanan
        self.filename = "data_laptop.csv"

        self.kebutuhan_map = {
            "Gaming": {"min_ram": 16, "min_storage": 512},
            "Office": {"min_ram": 4, "min_storage": 256},
            "Desain": {"min_ram": 8, "min_storage": 512}
        }

        self.setup_style()
        self.setup_ui()
        self.load_data() # Ganti seed_data() menjadi load_data()

    # ==========================================
    # FILE HANDLING (Menyimpan secara permanen)
    # ==========================================
    def load_data(self):
        """Membaca data dari file CSV saat aplikasi pertama kali dibuka"""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Pastikan baris memiliki 7 kolom data
                    if len(row) == 7:
                        # Convert data ke tipe yang benar (integer untuk id, ram, storage, harga)
                        id_laptop = int(row[0])
                        merk = row[1]
                        tipe = row[2]
                        ram = int(row[3])
                        storage = int(row[4])
                        harga = int(row[5])
                        kategori = row[6]
                        
                        laptop_baru = Laptop(id_laptop, merk, tipe, ram, storage, harga, kategori)
                        self.data_laptop.append(laptop_baru)
                        
                        # Update counter_id agar ID baru tidak bentrok dengan ID lama
                        if id_laptop >= self.counter_id:
                            self.counter_id = id_laptop + 1
            self.refresh_table()
        else:
            # Jika file belum ada (baru pertama kali buka aplikasi), isi data default
            self.create_laptop("ASUS", "ROG", 16, 1000, 20000000, "Gaming")
            self.create_laptop("Acer", "Swift", 4, 256, 6000000, "Office")
            self.create_laptop("Lenovo", "Thinkpad", 8, 512, 12000000, "Office")

    def save_data(self):
        """Menyimpan data dari Array ke dalam file CSV"""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for laptop in self.data_laptop:
                writer.writerow([laptop.id, laptop.merk, laptop.tipe, laptop.ram, laptop.storage, laptop.harga, laptop.kategori])

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#FFFFFF", foreground="#333333", rowheight=25, fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=('Helvetica', 9, 'bold'), background="#E1E8ED")
        style.map('Treeview', background=[('selected', '#007BFF')]) 
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TFrame", background=self.bg_color)

    def setup_ui(self):
        tab_control = ttk.Notebook(self.root)
        self.tab_crud = ttk.Frame(tab_control)
        self.tab_rekomendasi = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_crud, text='Kelola Data (CRUD)')
        tab_control.add(self.tab_rekomendasi, text='Cari Rekomendasi')
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.setup_crud_tab()
        self.setup_rekomendasi_tab()

    def setup_crud_tab(self):
        frame_input = tk.Frame(self.tab_crud, bg=self.bg_color)
        frame_input.pack(pady=15)

        def create_label(parent, text, row, col):
            tk.Label(parent, text=text, bg=self.bg_color, font=('Helvetica', 9)).grid(row=row, column=col, sticky="w", pady=5, padx=5)

        create_label(frame_input, "Merk:", 0, 0)
        self.entry_merk = ttk.Entry(frame_input)
        self.entry_merk.grid(row=0, column=1, pady=5, padx=5)

        create_label(frame_input, "Tipe:", 1, 0)
        self.entry_tipe = ttk.Entry(frame_input)
        self.entry_tipe.grid(row=1, column=1, pady=5, padx=5)

        create_label(frame_input, "RAM (GB):", 2, 0)
        self.entry_ram = ttk.Entry(frame_input)
        self.entry_ram.grid(row=2, column=1, pady=5, padx=5)

        create_label(frame_input, "Storage (GB):", 3, 0)
        self.entry_storage = ttk.Entry(frame_input)
        self.entry_storage.grid(row=3, column=1, pady=5, padx=5)

        create_label(frame_input, "Harga (Rp):", 4, 0)
        self.entry_harga = ttk.Entry(frame_input)
        self.entry_harga.grid(row=4, column=1, pady=5, padx=5)

        create_label(frame_input, "Kategori:", 5, 0)
        self.kategori_var = tk.StringVar(value="Office")
        self.combo_kategori = ttk.Combobox(frame_input, textvariable=self.kategori_var, values=["Office", "Gaming", "Desain"], state="readonly")
        self.combo_kategori.grid(row=5, column=1, pady=5, padx=5)

        frame_btn = tk.Frame(self.tab_crud, bg=self.bg_color)
        frame_btn.pack(pady=10)
        
        tk.Button(frame_btn, text="✚ Tambah Data", bg="#28A745", fg="white", font=('Helvetica', 9, 'bold'), relief="flat", padx=10, command=self.action_create).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="📝 Ubah Data", bg="#17A2B8", fg="white", font=('Helvetica', 9, 'bold'), relief="flat", padx=10, command=self.action_update).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="✖ Hapus Data", bg="#DC3545", fg="white", font=('Helvetica', 9, 'bold'), relief="flat", padx=10, command=self.action_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="⟲ Undo Hapus", bg="#FFC107", fg="black", font=('Helvetica', 9, 'bold'), relief="flat", padx=10, command=self.action_undo).pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Merk", "Tipe", "RAM", "Storage", "Harga", "Kategori")
        self.tree = ttk.Treeview(self.tab_crud, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_table_click)

    def setup_rekomendasi_tab(self):
        frame_filter = tk.Frame(self.tab_rekomendasi, bg=self.bg_color)
        frame_filter.pack(pady=20)

        tk.Label(frame_filter, text="Budget Maksimal (Rp):", bg=self.bg_color, font=('Helvetica', 9)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_budget = ttk.Entry(frame_filter, width=25)
        self.entry_budget.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filter, text="Kebutuhan Anda:", bg=self.bg_color, font=('Helvetica', 9)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rek_kategori_var = tk.StringVar(value="Office")
        ttk.Combobox(frame_filter, textvariable=self.rek_kategori_var, values=["Office", "Gaming", "Desain"], state="readonly", width=22).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_filter, text="🔍 Cari Rekomendasi", bg="#007BFF", fg="white", font=('Helvetica', 9, 'bold'), relief="flat", padx=20, pady=5, command=self.action_rekomendasi).grid(row=2, columnspan=2, pady=15)

        columns = ("Skor", "Merk", "Tipe", "RAM", "Storage", "Harga")
        self.tree_rek = ttk.Treeview(self.tab_rekomendasi, columns=columns, show="headings")
        for col in columns:
            self.tree_rek.heading(col, text=col)
            self.tree_rek.column(col, width=100, anchor="center")
        self.tree_rek.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

    def clear_form(self):
        self.entry_merk.delete(0, tk.END)
        self.entry_tipe.delete(0, tk.END)
        self.entry_ram.delete(0, tk.END)
        self.entry_storage.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)
        self.selected_laptop_id = None

    def on_table_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        row_data = self.tree.item(selected_item)['values']
        self.selected_laptop_id = int(row_data[0])
        
        self.entry_merk.delete(0, tk.END)
        self.entry_merk.insert(0, row_data[1])
        
        self.entry_tipe.delete(0, tk.END)
        self.entry_tipe.insert(0, row_data[2])
        
        self.entry_ram.delete(0, tk.END)
        self.entry_ram.insert(0, row_data[3])
        
        self.entry_storage.delete(0, tk.END)
        self.entry_storage.insert(0, row_data[4])
        
        harga_clean = str(row_data[5]).replace("Rp ", "").replace(",", "")
        self.entry_harga.delete(0, tk.END)
        self.entry_harga.insert(0, harga_clean)
        
        self.kategori_var.set(row_data[6])

    def create_laptop(self, merk, tipe, ram, storage, harga, kategori):
        laptop_baru = Laptop(self.counter_id, merk, tipe, ram, storage, harga, kategori)
        self.data_laptop.append(laptop_baru)
        self.counter_id += 1
        
        self.save_data() # Simpan data setelah ditambah
        self.refresh_table()

    def action_create(self):
        # 1. Ambil semua teks dan hapus spasi berlebih di awal/akhir menggunakan .strip()
        merk = self.entry_merk.get().strip()
        tipe = self.entry_tipe.get().strip()
        ram = self.entry_ram.get().strip()
        storage = self.entry_storage.get().strip()
        harga = self.entry_harga.get().strip()
        kategori = self.kategori_var.get().strip()

        # 2. VALIDASI KOSONG: Cek apakah ada satupun variabel yang masih kosong
        if not (merk and tipe and ram and storage and harga and kategori):
            messagebox.showwarning("Peringatan", "Semua kolom data wajib diisi, tidak boleh ada yang kosong!")
            return # Hentikan proses fungsi sampai di sini

        # 3. VALIDASI ANGKA: Coba masukkan ke dalam tabel
        try:
            self.create_laptop(merk, tipe, ram, storage, harga, kategori)
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan dan disimpan permanen!")
            self.clear_form()
        except ValueError:
            messagebox.showerror("Error", "Gagal menyimpan! Input RAM, Storage, dan Harga wajib berupa angka murni (tanpa huruf/titik/koma).")

    def action_update(self):
        if self.selected_laptop_id is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu yang ingin diubah!")
            return
        
        # 1. Ambil data
        merk = self.entry_merk.get().strip()
        tipe = self.entry_tipe.get().strip()
        ram = self.entry_ram.get().strip()
        storage = self.entry_storage.get().strip()
        harga = self.entry_harga.get().strip()
        kategori = self.kategori_var.get().strip()

        # 2. VALIDASI KOSONG
        if not (merk and tipe and ram and storage and harga and kategori):
            messagebox.showwarning("Peringatan", "Semua kolom data wajib diisi, tidak boleh ada yang kosong!")
            return
        
        # 3. VALIDASI ANGKA & PROSES UPDATE
        try:
            # Pastikan format angka aman sebelum ditimpa ke array
            ram_int = int(ram)
            storage_int = int(storage)
            harga_int = int(harga)

            # MATERI: Binary Search
            low, high = 0, len(self.data_laptop) - 1
            found_index = -1

            while low <= high:
                mid = (low + high) // 2
                if self.data_laptop[mid].id == self.selected_laptop_id:
                    found_index = mid
                    break
                elif self.data_laptop[mid].id < self.selected_laptop_id:
                    low = mid + 1
                else:
                    high = mid - 1

            if found_index != -1:
                self.data_laptop[found_index].merk = merk
                self.data_laptop[found_index].tipe = tipe
                self.data_laptop[found_index].ram = ram_int
                self.data_laptop[found_index].storage = storage_int
                self.data_laptop[found_index].harga = harga_int
                self.data_laptop[found_index].kategori = kategori
                
                self.save_data()
                self.refresh_table()
                messagebox.showinfo("Sukses", "Data laptop berhasil diperbarui dan disimpan!")
                self.clear_form()

        except ValueError:
            messagebox.showerror("Error", "Gagal memperbarui! Input RAM, Storage, dan Harga wajib berupa angka murni.")

    def action_delete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Klik/pilih salah satu data di tabel yang ingin dihapus terlebih dahulu!")
            return
        
        target_id = int(self.tree.item(selected_item)['values'][0])
        
        # 3. MATERI: Binary Search
        low, high = 0, len(self.data_laptop) - 1
        found_index = -1

        while low <= high:
            mid = (low + high) // 2
            if self.data_laptop[mid].id == target_id:
                found_index = mid
                break
            elif self.data_laptop[mid].id < target_id:
                low = mid + 1
            else:
                high = mid - 1

        if found_index != -1:
            laptop_dihapus = self.data_laptop.pop(found_index)
            self.stack_undo.append(laptop_dihapus)
            
            self.save_data() # Perbarui file penyimpanannya
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Sukses", f"Data '{laptop_dihapus.merk} {laptop_dihapus.tipe}' dihapus!\n\n(Bisa dibatalkan dengan tombol Undo)")

    def action_undo(self):
        if not self.stack_undo:
            messagebox.showinfo("Info", "Tidak ada riwayat data yang dihapus untuk dikembalikan!")
            return
        
        laptop_dikembalikan = self.stack_undo.pop()
        self.data_laptop.append(laptop_dikembalikan)
        self.data_laptop.sort(key=lambda x: x.id) 
        
        self.save_data() # Perbarui penyimpanan setelah data kembali
        self.refresh_table()
        messagebox.showinfo("Sukses", f"Data '{laptop_dikembalikan.merk} {laptop_dikembalikan.tipe}' berhasil dipulihkan dan tersimpan!")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for laptop in self.data_laptop:
            harga_format = f"Rp {laptop.harga:,}"
            self.tree.insert("", tk.END, values=(laptop.id, laptop.merk, laptop.tipe, laptop.ram, laptop.storage, harga_format, laptop.kategori))

    # --- FUNGSI REKOMENDASI ---
    def action_rekomendasi(self):
        try:
            budget = int(self.entry_budget.get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan nominal budget menggunakan angka (Contoh: 10000000)")
            return

        kebutuhan = self.rek_kategori_var.get()
        syarat = self.kebutuhan_map[kebutuhan]
        hasil_rekomendasi = []

        # 4. MATERI: Linear Search
        for laptop in self.data_laptop:
            if laptop.harga <= budget:
                skor = 0
                if laptop.kategori == kebutuhan: skor += 50
                if laptop.ram >= syarat["min_ram"]: skor += 25
                if laptop.storage >= syarat["min_storage"]: skor += 25
                
                if skor > 0:
                    hasil_rekomendasi.append([skor, laptop])

        # 5. MATERI: Selection Sort 
        n = len(hasil_rekomendasi)
        for i in range(n):
            max_idx = i
            for j in range(i + 1, n):
                if hasil_rekomendasi[j][0] > hasil_rekomendasi[max_idx][0]:
                    max_idx = j
            hasil_rekomendasi[i], hasil_rekomendasi[max_idx] = hasil_rekomendasi[max_idx], hasil_rekomendasi[i]

        for row in self.tree_rek.get_children():
            self.tree_rek.delete(row)
        for skor, laptop in hasil_rekomendasi:
            harga_format = f"Rp {laptop.harga:,}"
            self.tree_rek.insert("", tk.END, values=(skor, laptop.merk, laptop.tipe, laptop.ram, laptop.storage, harga_format))

if __name__ == "__main__":
    root = tk.Tk()
    app = RekomendasiLaptopApp(root)
    root.mainloop()
