from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import font
import ctypes
import threading
import time
import os
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.signal import savgol_filter
import pandas as pd

"""
@file: GUI_Spektroscreen.py
@description: Script ini digunakan sebagai interface spektrofotometer untuk pengambilan data.
@date: 2024-08-26
@version: 1.0
@copyright: 2024, Muhammad Ridho Pratama. All rights reserved.
"""

# Buka file teks dalam mode baca ('r')
with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
    # Baca seluruh isi file dan simpan dalam variabel
    file_contents = file.readlines()

wd = tb.Window(themename= "darkly")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [int((0.85*user32.GetSystemMetrics(0))), int((0.9*user32.GetSystemMetrics(1)))]

wd.geometry(str(w)+'x'+str(h))
wd.title("Spectroscreen V.1")


wd.pack_propagate(False)
wd.resizable(0, 0) # Lebar layar tidak bisa diubah

file_path_general = "/".join(os.path.abspath(__file__).split('\\')[:-1])


icon_apk_ = Image.open(os.path.join(file_path_general,"icon/icon.png").replace('\\', '/'))  
icon_apk_ = icon_apk_.resize((20, 20))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_apk = ImageTk.PhotoImage(icon_apk_)

wd.iconphoto(False, icon_apk)
icon_plus_ = Image.open(os.path.join(file_path_general,"icon/plus.png").replace('\\', '/'))  
icon_plus_ = icon_plus_.resize((20, 20))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_plus = ImageTk.PhotoImage(icon_plus_)

icon_hapus_ = Image.open(os.path.join(file_path_general,"icon/delete.png").replace('\\', '/'))  
icon_hapus_ = icon_hapus_.resize((20, 20))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_hapus = ImageTk.PhotoImage(icon_hapus_)

icon_apply_ = Image.open(os.path.join(file_path_general,"icon/checked.png").replace('\\', '/'))  
icon_apply_ = icon_apply_.resize((18, 18))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_apply = ImageTk.PhotoImage(icon_apply_)

icon_sv_graph_ = Image.open(os.path.join(file_path_general,"icon/save_.png").replace('\\', '/'))  
icon_sv_graph_ = icon_sv_graph_.resize((18, 18))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_sv_graph = ImageTk.PhotoImage(icon_sv_graph_)

icon_sv_pict_ = Image.open(os.path.join(file_path_general,"icon/camera_.png").replace('\\', '/'))  
icon_sv_pict_ = icon_sv_pict_.resize((35, 35))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_sv_pict = ImageTk.PhotoImage(icon_sv_pict_)

icon_change_ = Image.open(os.path.join(file_path_general,"icon/shuffle.png").replace('\\', '/'))  
icon_change_ = icon_change_.resize((20, 20))  # Menyesuaikan ukuran gambar sesuai kebutuhan
icon_change = ImageTk.PhotoImage(icon_change_)



# Menubar
mb = Menu(wd)
wd.config(menu = mb)

# File
def search_file():
    global  df, dataset_file
    #global filename, wdd
    filename = filedialog.askopenfilename(initialdir="/".join(os.path.abspath(__file__).split('\\')[:-1]),
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    #wdd["text"] = filename
        
    try:
        dataset_file = r"{}".format(filename)
        if dataset_file[-4:] == ".csv": #Mendapatkan 4 karakter ekstensi file yang diambil (misal .csv yang berjumlah 4)
            df = pd.read_csv(dataset_file)
            
        else:
            df = pd.read_excel(dataset_file)
            

    except ValueError:
        messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        messagebox.showerror("Information", f"No such file {dataset_file}")
        return None
    
    tampil_data()

    btn_plus['state'] = 'normal'
    btn_plus_col['state'] = 'normal'
    btn_hapus['state'] = 'normal'
    btn_change['state'] = 'normal'
    
    return df

def tampil_data():
    global df
    clear_data()
    data["column"] = list(df.columns)
    data["show"] = "headings"
    for column in data["columns"]:
        data.column(column, width=50, anchor='center')
        data.heading(column, text=column, anchor = 'center') # let the column heading = column name

    #df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    
    for i, row in df.iterrows():
        data.insert("", "end", values=list(row), tags=(f"row_{i}",))

    data.bind("<ButtonRelease-1>", on_click_data)
    
    
    

def on_click_data(event):
    global row_idx, col_idx, col_name, ent_kolom, ent_baris, var_hapus_data, ent_tambah_kolom_idx, ent_tambah_nama_kolom, ent_baris_change, ent_kolom_change, ent_var_lama
    item = event.widget.focus()  # Mendapatkan item (baris) yang dipilih
    
    row_idx = int(event.widget.item(item, "tags")[0].split("_")[1])  # Mendapatkan nomor baris dari tag
    col_idx = event.widget.identify_column(event.x)  # Mendapatkan nama kolom dari posisi klik
    col_name = event.widget.heading(col_idx)["text"]  # Mendapatkan teks heading (nama kolom) dari kolom

    
    if stat_perubahan == 3:
        ent_baris.delete(0, tb.END)
        ent_kolom.delete(0, tb.END)
        if var_hapus_data.get() == "B":
            ent_baris.insert(tb.END, str(row_idx))
            #ent_kolom.delete(0, tb.END)
        if var_hapus_data.get() == "K":
            #ent_baris.delete(0, tb.END)
            ent_kolom.insert(tb.END, col_name)
        if var_hapus_data.get() == "E":
            ent_baris.insert(tb.END, str(row_idx))
            ent_kolom.insert(tb.END, col_name)
    
    if stat_perubahan ==2:
        ent_tambah_kolom_idx['state'] = 'normal'
        ent_tambah_kolom_idx.delete(0, tb.END)
        ent_tambah_kolom_idx.insert(0, col_name)
        ent_tambah_kolom_idx['state'] = 'disabled'
        ent_tambah_nama_kolom['state'] = 'normal'

    if stat_perubahan == 4:
        ent_baris_change['state'] = 'normal'
        ent_kolom_change['state'] = 'normal'
        ent_var_lama['state'] = 'normal'
        ent_baris_change.delete(0, tb.END)
        ent_kolom_change.delete(0, tb.END)
        ent_var_lama.delete(0, tb.END)
        ent_baris_change.insert(tb.END, str(row_idx))
        ent_kolom_change.insert(tb.END, col_name)
        ent_var_lama.insert(tb.END, df[col_name][row_idx])
        ent_baris_change['state'] = 'disabled'
        ent_kolom_change['state'] = 'disabled'
        ent_var_lama['state'] = 'disabled'
        ent_new_var['state'] = 'normal'


# Fungsi untuk menangani penutupan jendela
def on_closing():
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
        cap.release()  
        wd.destroy()  

def clear_data():
    data.delete(*data.get_children())
    return None

def save_excel_file():
    global file_path, dataset_file, data
    #filedialog.asksaveasfilename(title="Spektrum Referensi", initialfile="Spektrum Referensi.xlsx", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")])

    if 'df' in globals():
        file_path = filedialog.asksaveasfilename(initialfile=dataset_file.split('/')[-1], defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")])

        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showwarning("File Tersimpan", "File berhasil disimpan")
            for row in data.get_children():
                data.delete(row)
    else:
        messagebox.showwarning("File tidak tersedia", "Tidak ada file yang dibuka untuk disimpan")
        pass

    return file_path

    

def create_new():
    global x_data_plot, file_path, df, dataset_file
    
    with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
            file.writelines(file_contents)
    nilai_presisi_data = file_contents[13].split(" ")
    data_kolom = np.round(x_data_plot, int(nilai_presisi_data[0]))

    df = pd.DataFrame(columns= data_kolom)
    #print(df)

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")])

    if file_path:
        df.to_excel(file_path, index=False)
    

    try:
        dataset_file = r"{}".format(file_path)
        if dataset_file[-4:] == ".csv": #Mendapatkan 4 karakter ekstensi file yang diambil (misal .csv yang berjumlah 4)
            df = pd.read_csv(dataset_file)
            
        else:
            df = pd.read_excel(dataset_file)
    
        
            

    except ValueError:
        messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        messagebox.showerror("Information", f"No such file {file_path}")
        return None
    
    tampil_data()

    btn_plus['state'] = 'normal'
    btn_plus_col['state'] = 'normal'
    btn_hapus['state'] = 'normal'
    btn_change['state'] = 'normal'

def file_ref():
    global file_contents
    file_ref_path = filedialog.askopenfilename(initialdir="/".join(os.path.abspath(__file__).split('\\')[:-1]),
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    
    if file_ref_path.strip() and not file_ref_path.isspace():
        file_contents[9] = file_ref_path + '\n'
        with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
            file.writelines(file_contents)
        with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
            # Baca seluruh isi file dan simpan dalam variabel
            file_contents = file.readlines()

def save_file_ref():
    global file_contents, x_data_plot, y_data_plot
    nilai_presisi_data = file_contents[13].split(" ")
    data_kolom_file_ref = np.round(x_data_plot, int(nilai_presisi_data[0]))

    df_file_ref = pd.DataFrame(columns= data_kolom_file_ref)
    df_file_ref.loc[len(df_file_ref)] = y_data_plot
    
    file_ref_path = filedialog.asksaveasfilename(title="Spektrum Referensi", initialfile="Spektrum Referensi.xlsx", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")])

    if file_ref_path:
        df_file_ref.to_excel(file_ref_path, index=False)

def file_amb():
    global file_contents
    file_amb_path = filedialog.askopenfilename(initialdir="/".join(os.path.abspath(__file__).split('\\')[:-1]),
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    if file_amb_path.strip() and not file_amb_path.isspace():
        file_contents[11] = file_amb_path + '\n'
        with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
            file.writelines(file_contents)
        with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
            # Baca seluruh isi file dan simpan dalam variabel
            file_contents = file.readlines()

def save_file_amb():
    global file_contents

    nilai_presisi_data = file_contents[13].split(" ")
    data_kolom_file_amb = np.round(x_data_plot, int(nilai_presisi_data[0]))

    df_file_amb = pd.DataFrame(columns= data_kolom_file_amb)
    df_file_amb.loc[len(df_file_amb)] = y_data_plot
    
    file_amb_path = filedialog.asksaveasfilename(title="Intensitas Lingkungan", initialfile="Intensitas Lingkungan.xlsx", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")])
    if file_amb_path:
        df_file_amb.to_excel(file_amb_path, index=False)
    

def sv_angka_presisi():
    global file_contents
    presisi_xt = file_contents[13].split(" ")[0]
    presisi_yt = file_contents[13].split(" ")[1]
    if presisi_x.get().strip() and not presisi_x.get().isspace():
        presisi_xt = presisi_x.get()

    if presisi_y.get().strip() and not presisi_y.get().isspace():
        presisi_yt = presisi_y.get()
        
    file_contents[13] = presisi_xt + " " + presisi_yt +'\n'
    with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
        file.writelines(file_contents)

    with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:# Baca seluruh isi file dan simpan dalam variabel
        file_contents = file.readlines()

def set_presisi():
    global file_contents, new_window_presisi, presisi_x, presisi_y
    new_window_presisi = tb.Toplevel(wd)
    new_window_presisi.title("Set Jumlah Nilai Presisi")
    new_window_presisi.geometry(str(int(0.25*w))+"x"+str(int(0.17*h)))
    new_window_presisi.iconphoto(False, icon_apk)
    menu_sett.entryconfig("Atur Angka Presisi", state="disabled")
    new_window_presisi.protocol("WM_DELETE_WINDOW", on_wd_setpresisi_close)
    new_window_presisi.resizable(0, 0)
    lbl_p1 = tb.Label(new_window_presisi, text= "sb X : ", bootstyle = "info", font = ("Verdana", 9))
    lbl_p1.place(relx = 0.02, rely = 0.2)
    presisi_x = tb.Spinbox(new_window_presisi, bootstyle = 'warning', from_=2, to=12, width = 6)
    presisi_x.place(relx= 0.16, rely = 0.15)
    lbl_p2 = tb.Label(new_window_presisi, text= "sb Y : ", bootstyle = "info", font = ("Verdana", 9))
    lbl_p2.place(relx = 0.55, rely = 0.2)
    btn_p2 = tb.Button(new_window_presisi, bootstyle = 'light-outline', state = 'normal', image = icon_sv_graph, command=sv_angka_presisi)
    btn_p2.place(relx= 0.16, rely = 0.5)
    presisi_y = tb.Spinbox(new_window_presisi, bootstyle = 'warning', from_=2, to=12, width = 6)
    presisi_y.place(relx= 0.7, rely = 0.15)
    presisi_x.set(int(file_contents[13].split(" ")[0]))
    presisi_y.set(int(file_contents[13].split(" ")[1]))

def on_wd_setpresisi_close():
    new_window_presisi.destroy()
    menu_sett.entryconfig('Atur Angka Presisi', state = 'normal')

def set_savgol():
    global file_contents, param1, param2

    _savgol_param = [sb_WL.get(), sb_OP.get()]
    savgol_param0 = file_contents[15].split(" ")
    param1, param2 = int(savgol_param0[0]), int(savgol_param0[1])

    for idx, val in enumerate(_savgol_param):
        if val.strip() and not val.isspace():
            if idx == 0:
                param1 = val
            if idx == 1:
                param2 = val

    file_contents[15] = str(param1) + " " + str(param2) + "\n"

    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
        file.writelines(file_contents)

    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
        file_contents = file.readlines()
    


def toggle_stat_savgol():
    global file_contents
    
    if var_status_savgol.get() == True:
        file_contents[17] = '1'
    
    if var_status_savgol.get() == False:
        file_contents[17] = '0'
        
    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
        file.writelines(file_contents)

def on_wd_savgol_close():
    new_window_savgol.destroy()
    mn1.entryconfig('Filter Sav-Gol', state = 'normal')

def atur_sav_gol():
    global file_contents, new_window_savgol, var_status_savgol, sb_WL, sb_OP
    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
        # Baca seluruh isi file dan simpan dalam variabel
        file_contents = file.readlines()
    new_window_savgol = tb.Toplevel(wd)
    new_window_savgol.title("Filter Savitzky Golay")
    new_window_savgol.geometry(str(int(0.25*w))+"x"+str(int(0.17*h)))
    new_window_savgol.iconphoto(False, icon_apk)
    mn1.entryconfig('Filter Sav-Gol', state="disabled")
    new_window_savgol.protocol("WM_DELETE_WINDOW", on_wd_savgol_close)
    new_window_savgol.resizable(0, 0)
    lbl_WL = tb.Label(new_window_savgol, text= "Lebar Window : ", bootstyle = "info", font = ("Verdana", 9))
    lbl_WL.place(relx = 0.08, rely = 0.1)
    sb_WL = tb.Spinbox(new_window_savgol, bootstyle = 'warning', from_=2, to=len(x_data_plot), width = 6)
    sb_WL.place(relx= 0.09, rely = 0.25)
    lbl_OP = tb.Label(new_window_savgol, text= "Orde Polinom : ", bootstyle = "info", font = ("Verdana", 9))
    lbl_OP.place(relx = 0.54, rely = 0.1)
    sb_OP = tb.Spinbox(new_window_savgol, bootstyle = 'warning', from_=1, to=len(x_data_plot)-1, width = 6)
    sb_OP.place(relx= 0.55, rely = 0.25)

    lbl_catatan = tb.Label(new_window_savgol, text= "catatan : orde polinom < lebar window", bootstyle = "info", font = ("Verdana", 9))
    lbl_catatan.place(relx = 0.08, rely = 0.5)
    btn_sv_savgol = tb.Button(new_window_savgol, bootstyle = 'light-outline', state = 'normal', image = icon_sv_graph, command=set_savgol)
    btn_sv_savgol.place(relx= 0.09, rely = 0.7)
    
    #print(file_contents[15].split(" "))
    sb_WL.set(int(file_contents[15].split(" ")[0]))
    sb_OP.set(int(file_contents[15].split(" ")[1]))
    var_status_savgol = BooleanVar()
    if int(file_contents[17]) == 0:
        var_status_savgol.set(False)
    if int(file_contents[17]) == 1:
        var_status_savgol.set(True)
    cb_status_savgol = tb.Checkbutton(new_window_savgol, bootstyle = 'warning-round_toggle', text = "Terapkan", variable = var_status_savgol, state= 'normal', command = toggle_stat_savgol)
    cb_status_savgol.place(relx = 0.55, rely = 0.7)


def on_wd_tentang():
    new_window_tentang.destroy()
    mn2.entryconfig('Tentang Kami', state = 'normal')

def tentang():
    global new_window_tentang
    new_window_tentang = tb.Toplevel(wd)
    new_window_tentang.title("Spectroscreen V.1")
    new_window_tentang.geometry(str(int(0.3*w))+"x"+str(int(0.3*h)))

    new_window_tentang.iconphoto(False, icon_apk)
    mn2.entryconfig('Informasi', state="disabled")
    new_window_tentang.protocol("WM_DELETE_WINDOW", on_wd_tentang)
    new_window_tentang.resizable(0, 0)

    label_ttg = tb.Label(new_window_tentang, text= "Info", bootstyle = "info", font = ("Verdana", 9))
    label_ttg.place(relx = 0.03, rely = 0.05)

    #info_frame = tb.LabelFrame(new_window_tentang, text = "Info", bootstyle = "warning")
    #info_frame.place(height = 0.75*int(0.3*h), width = 0.95*int(0.3*w), rely = 0.15, relx = 0.02) 
    
    teks_info = "Grafis antarmuka ini dirancang untuk mengumpulkan data spektral dari spektrofotometer dalam bentuk data tabular. Data tabular tersebut pada awalnya dimaksudkan untuk mempermudah proses pelatihan Machine Learning. Antarmuka ini juga mendukung input gambar, baik melalui USB maupun melalui tautan sumber kamera.  \n\nNama Karya     : GUI Spektroscreen V.1 \nPemberi Lisensi : Muhammad Ridho Pratama (Juli 2024) \nGitHub              : https://github.com/MRidhoPratama251"
    text_widget = tb.Text(new_window_tentang, wrap='word', font=("Verdana", 9))
    text_widget.insert(tb.END, teks_info)
    text_widget.config(state='disabled')  # Agar teks tidak bisa diedit
    text_widget.place(height = int(0.7*int(0.3*h)), width = int(0.95*int(0.3*w)), relx = 0.02, rely = 0.15)

    #label_git = tb.Label(new_window_tentang, text= "GitHub : https://github.com/MRidhoPratama251", bootstyle = "info", font = ("Verdana", 9))
    #label_git.place(relx = 0.03, rely = 0.88)
    



mn0 = Menu(mb, tearoff = 0)
mb.add_cascade(label = "File", menu = mn0)

menu_File = Menu(mb, tearoff = 0)
mn0.add_command(label = "Create New", command = create_new)
mn0.add_command(label = "Open File", command = search_file)
mn0.add_command(label = "Save File", command = save_excel_file)
mn0.add_command(label = "Exit", command = on_closing)
mn0.add_separator()

menu_sett = Menu(mn0, tearoff=0)
mn0.add_cascade(label = "Setting", menu = menu_sett)
menu_sett.add_command(label = 'File Referensi', command = file_ref)
menu_sett.add_command(label = 'Save File Referensi', command = save_file_ref)
menu_sett.add_command(label = 'File Ambient', command = file_amb)
menu_sett.add_command(label = 'Save File Ambient', command = save_file_amb)
menu_sett.add_command(label = 'Atur Angka Presisi', command = set_presisi)


mn1 = Menu(mb, tearoff = 0)
mb.add_cascade(label = 'Alat', menu = mn1)

menu_alat = Menu(mb, tearoff = 0)
mn1.add_command(label = 'Filter Sav-Gol', command = atur_sav_gol)


mn2 = Menu(mb, tearoff = 0)
mb.add_cascade(label = 'Tentang', menu = mn2)
mn2.add_command(label = 'Informasi', command = tentang)

### ==== LabelFrame ==== ###

ctr_frame = tb.LabelFrame(wd, text = "Kontrol", bootstyle = "warning")
ctr_frame.place(height = 0.51*h, width = 0.4*w, rely = 0.01, relx = 0.01) #height = 350, width = 590

cam_frame = tb.LabelFrame(wd, text = "Kamera", bootstyle = "warning")
cam_frame.place(height = 0.51*h, width = 0.54*w, rely = 0.01, relx = 0.45) #height = 350, width = 590

### === Control === ###

## Kalibrasi
tp = [float(value) for value in file_contents[5].split()]
pos_tp1, pos_tp2 = tp[0], tp[1]

def linear_mapping(x, x_min, x_max, xnew_min, xnew_max):
    try:
        percentage = (x - x_min) / (x_max - x_min)
        x_new = xnew_min + percentage * (xnew_max - xnew_min)
    except ZeroDivisionError:
        x_new = x
    return x_new

def simpan_kalibrasi():
    global status_loop, x_limit, ROI, x_data_plot, idx1, idx2, x_data_new, file_contents, x_nearest #axvline1, axvline2#, show_graph##show_graph #axvline1, axvline2
    btn_kalib['text'] = 'Kalibrasi'
    btn_kalib['command'] = Kalibrasi
    var1.set(False)
    var2.set(False)
    with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
    # Baca seluruh isi file dan simpan dalam variabel
        file_contents = file.readlines()
    
    tp = [float(value) for value in file_contents[5].split()]
    #pos_tp1, pos_tp2 = tp[0], tp[1]
    #print(trim_point1.get() == " ", trim_point2.get() == "")
    
    if trim_point1.get() != "" and trim_point2.get() != "":
        file_contents[5] = trim_point1.get() + " " + trim_point2.get() + "\n"
        x_data_new = linear_mapping(x_data_plot, x_data_plot[idx1], x_data_plot[idx2], float(trim_point1.get()), float(trim_point2.get()))
        
    
    if trim_point1.get() != ""  and trim_point2.get() == "" :
        file_contents[5] = trim_point1.get() + " " + str(tp[1])
        x_data_new = linear_mapping(x_data_plot, x_data_plot[idx1], x_data_plot[idx2], float(trim_point1.get()), tp[1])
        
    if trim_point1.get() == ""  and trim_point2.get() != "" :
        file_contents[5] = str(tp[0]) + " " + trim_point2.get()
        x_data_new = linear_mapping(x_data_plot, x_data_plot[idx1], x_data_plot[idx2], tp[0], float(trim_point2.get()))

    if trim_point1.get() == ""  and trim_point2.get() == "":
        pass

    try:
        if str(x_data_new[0]) != "-inf" or str(x_data_new[-1]) != "inf":
            x_limit = [x_data_new[0], x_data_new[-1]]
            file_contents[3] = str(x_limit[0]) + " " + str(x_limit[-1]) + "\n"
            with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
                file.writelines(file_contents)
    except NameError:
        pass
    trim_point1.delete('0', 'end')
    trim_point2.delete('0', 'end')
    lbl_tp1['text'] = 'Titik 1 :'
    lbl_tp2['text'] = 'Titik 2 :'

        
        
def Kalibrasi():
    global pos_tp1, pos_tp2, status_loop, x_nearest, idx1, idx2, x_data_plot
    c_tp1['state'] = 'normal'
    btn_kalib['text'] = 'Simpan'
    btn_kalib['command'] = simpan_kalibrasi

    
    if var1.get() is False : 
        trim_point2['state'] = 'disabled'
        c_tp2['state'] = 'disabled'
        try :            
            idx1 = np.where(x_data_plot == x_nearest)[0][0]
            lbl_tp1['text'] = 'Titik 1 : ' + str(round(x_nearest, 3))
        except NameError:
            pass
        except IndexError:
            pass

    if var1.get() is True:
        c_tp2['state'] = 'normal'
        trim_point1['state'] = 'disabled'
        lbl_tp1['text'] = 'Titik 1 : ' + trim_point1.get()
        try :
            idx2 = np.where(x_data_plot == x_nearest)[0][0]
            lbl_tp2['text'] = 'Titik 2 : ' + str(round(x_nearest, 3))
        except NameError:
            pass
        except IndexError:
            pass

    if var2.get() is False:
        btn_kalib['state'] = 'disabled'
        status_loop = False

    if var2.get() is True:
        trim_point2['state'] = 'disabled'
        c_tp1['state'] = 'disabled'
        c_tp2['state'] = 'disabled'
        lbl_tp2['text'] = 'Titik 2 : ' + trim_point2.get()
        btn_kalib['state'] = 'normal'
        status_loop = True
    
    if not status_loop:
        wd.after(15, Kalibrasi)


status_loop = False
kalib_frame = tb.LabelFrame(ctr_frame, text = 'Kalibrasi', bootstyle = 'danger')
kalib_frame.place(height = 0.27*(0.5*h), width = 0.9*(0.4*w), rely = 0.001, relx = 0.05)

trim_point1 = tb.Entry(kalib_frame, bootstyle = "info", state = 'disabled', width = 8, font = ("Helvetica", 8))
trim_point1.place(relx = 0.05, rely = 0.26)
lbl_tp1 = tb.Label(kalib_frame, text= "Titik 1 : ", bootstyle = "info", font = ("Verdana", 8))
lbl_tp1.place(relx = 0.05, rely = 0.65)
 

trim_point2 = tb.Entry(kalib_frame, bootstyle = "info", state = 'disabled', width = 8, font = ("Helvetica", 8))
trim_point2.place(relx = 0.4, rely = 0.26)
lbl_tp2 = tb.Label(kalib_frame, text= "Titik 2 : ", bootstyle = "info", font = ("Verdana", 8))
lbl_tp2.place(relx = 0.4, rely = 0.65)

btn_kalib = tb.Button(kalib_frame, text = 'Kalibrasi', bootstyle = 'light-outline', width = 9, command = Kalibrasi)
btn_kalib.place(relx= 0.77, rely = 0.26)

var1 = BooleanVar()
c_tp1 = tb.Checkbutton(kalib_frame, text = 'Titik 1', bootstyle = 'info', variable = var1, state = 'disabled')
c_tp1.place(relx = 0.05, rely = 0.01)

var2 = BooleanVar()
c_tp2 = tb.Checkbutton(kalib_frame, text = 'Titik 2', bootstyle = 'info', variable = var2, state = 'disabled')
c_tp2.place(relx = 0.4, rely = 0.01)

### Pilih Sensor Kamera
def save_change():
    global cap, file_contents

    btn_select_cam['text'] = 'Pilih'
    btn_select_cam['command'] = select_sensor
    port_cam['state'] = 'disabled'
    try:
        port = int(port_cam.get())
    except ValueError:
        port = port_cam.get()
    
    if port != "":
        cap = cv2.VideoCapture(port)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_cam)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_cam)
        file_contents[7] = str(port) + '\n'
        with open(os.path.join("/".join(os.path.abspath(__file__).split('\\')[:-1]),'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
            file.writelines(file_contents)

def select_sensor():
    btn_select_cam['text'] = 'Simpan'
    btn_select_cam['command'] = save_change
    port_cam['state'] = 'normal' 


select_cam = tb.LabelFrame(ctr_frame, text = 'Pilih Sensor Kamera', bootstyle = 'danger')
select_cam.place(height = 0.15*(0.5*h), width = 0.9*(0.4*w), rely = 0.28, relx = 0.05)

lbl_cam_port = tb.Label(select_cam, text= "Kamera port : ", bootstyle = "info", font = ("Verdana", 9))
lbl_cam_port.place(relx = 0.05, rely = 0.2)

port_cam = tb.Entry(select_cam, bootstyle = "info", state = 'disabled', width = 20, font = ("Verdana", 9))
port_cam.place(relx = 0.28, rely = 0.07)

btn_select_cam = tb.Button(select_cam, text = 'Pilih', bootstyle = 'light-outline', width = 9, command = select_sensor)
btn_select_cam.place(relx= 0.77, rely = 0.07)


### Pengaturan Data
def clear_ds_frame_set():
    for widget in ds_frame_set.winfo_children():
        widget.destroy()

def add_entry_value():
    global ls_val, idx_values, isi_kolom

    ls_val[idx_values] = isi_kolom.get()

def clear_entry(event):
    global ls_val, idx_values, isi_kolom, cb_kolom_
    isi_kolom.delete(0, tb.END)
    idx_values = list(cb_kolom_['values']).index(cb_kolom_.get())
    isi_kolom.insert(tb.END, ls_val[idx_values])

def tambah_data():
    global df, isi_kolom, cb_kolom_, ls_val, stat_perubahan, constant_, var_tambah_spektrum, var_jenis_data, numeric_indices, string_indices, kolom_string, kolom_numerik
    btn_plus_col['state'] = 'disabled'
    btn_hapus['state'] = 'disabled'
    btn_change['state'] = 'disabled'

    kolom_df = df.columns
    kolom_string = [value for value in kolom_df if str(value).isalpha()]
    kolom_numerik = [value for value in pd.to_numeric(kolom_df, errors='coerce') if not pd.isnull(value)] 
    numeric_indices = []
    string_indices = []

    idx_random = np.random.randint(0, len(kolom_numerik), 5)
    num_to_str = list(map(str, kolom_numerik))
    panjang_dibelakang_koma = [len(num_to_str[idx].split('.')[1]) for idx in idx_random]
    constant_ = np.max(panjang_dibelakang_koma)


    for i, value in enumerate(kolom_df):
        try:
            pd.to_numeric(value)
            numeric_indices.append(i)
        except ValueError:
            string_indices.append(i)

    cb_kolom_ = tb.Combobox(ds_frame_set, values = kolom_string, bootstyle = 'warning', width = 9)
    cb_kolom_.place(relx = 0.4, rely = 0.01)
    cb_kolom_.bind("<<ComboboxSelected>>", clear_entry)

    isi_kolom = tb.Entry(ds_frame_set, bootstyle = "info", state = 'normal', width = 11, font = ("Verdana", 8))
    isi_kolom.place(relx = 0.4, rely = 0.5)

    btn_saveisikolom = tb.Button(ds_frame_set, bootstyle = 'light-outline', state = 'normal', image = icon_plus, command=add_entry_value)
    btn_saveisikolom.place(relx= 0.63, rely = 0.5)

    ls_val = [""]*len(kolom_string)
    
    if len(string_indices) != 0:
        isi_kolom['state'] = 'normal'
    if len(string_indices) == 0:
        isi_kolom['state'] = 'disabled'

    

    var_jenis_data = StringVar()
    var_jenis_data.set("I")
    r_I = tb.Radiobutton(ds_frame_set, text = 'Intensitas', bootstyle = 'warning', variable = var_jenis_data, value = 'I')
    r_I.place(relx = 0.02, rely = 0.05)
    r_A = tb.Radiobutton(ds_frame_set, text = 'Absorbsi', bootstyle = 'warning', variable = var_jenis_data, value = 'A')
    r_A.place(relx = 0.02, rely = 0.3)

    if var_status_A.get() == True:
        r_A['state'] = 'normal'

    if var_status_A.get() == False:
        r_A['state'] = 'disabled'

    var_tambah_spektrum = BooleanVar()
    var_tambah_spektrum.set(False)
    c_tambah_spektrum = tb.Checkbutton(ds_frame_set, text = 'Tambah Spektrum', bootstyle = 'info', variable = var_tambah_spektrum, state = 'normal')
    c_tambah_spektrum.place(relx = 0.02, rely = 0.6)
    stat_perubahan = 1
    btn_simpan_perubahan['state'] = 'normal'
    #pass

def tambah_kolom():
    global stat_perubahan, ent_tambah_kolom_idx, ent_tambah_nama_kolom
    btn_plus['state'] = 'disabled'
    btn_hapus['state'] = 'disabled'
    btn_change['state'] = 'disabled'

    lbl_tambah_kolom = tb.Label(ds_frame_set, text= "Posisi Kolom :", bootstyle = "info", font = ("Verdana", 9))
    lbl_tambah_kolom.place(relx = 0.05, rely = 0.15)

    ent_tambah_kolom_idx = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 15, font = ("Verdana", 8))
    ent_tambah_kolom_idx.place(relx = 0.35, rely = 0.1)

    lbl_tambah_nama_kolom = tb.Label(ds_frame_set, text= "Nama Kolom :", bootstyle = "info", font = ("Verdana", 9))
    lbl_tambah_nama_kolom.place(relx = 0.05, rely = 0.55)

    ent_tambah_nama_kolom = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 15, font = ("Verdana", 8))
    ent_tambah_nama_kolom.place(relx = 0.35, rely = 0.5)

    stat_perubahan = 2
    btn_simpan_perubahan['state'] = 'normal'

def jenis_hapus():
    global ent_baris, ent_kolom, var_hapus_data
    ent_baris.delete(0, tb.END)
    ent_kolom.delete(0, tb.END)

    if var_hapus_data.get() == 'B':
        ent_baris['state'] = 'normal'
        ent_kolom['state'] = 'disabled'

    if var_hapus_data.get() == 'K':
        ent_kolom['state'] = 'normal'
        ent_baris['state'] = 'disabled'

    if var_hapus_data.get() == 'E':
        ent_kolom['state'] = 'normal'
        ent_baris['state'] = 'normal'
        


def hapus_data():
    global stat_perubahan, ent_baris, ent_kolom, var_hapus_data
    btn_plus_col['state'] = 'disabled'
    btn_plus['state'] = 'disabled'
    btn_change['state'] = 'disabled'


    lbl_baris = tb.Label(ds_frame_set, text= "Baris       :", bootstyle = "info", font = ("Verdana", 9))
    lbl_baris.place(relx = 0.4, rely = 0.15)
    lbl_kolom = tb.Label(ds_frame_set, text= "Kolom     :", bootstyle = "info", font = ("Verdana", 9))
    lbl_kolom.place(relx = 0.4, rely = 0.6)


    ent_baris = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 15, font = ("Verdana", 8))
    ent_baris.place(relx = 0.6, rely = 0.15)
    ent_kolom = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 15, font = ("Verdana", 8))
    ent_kolom.place(relx = 0.6, rely = 0.6)

    var_hapus_data = StringVar()
    var_hapus_data.set("B")
    r_baris = tb.Radiobutton(ds_frame_set, text = 'Baris', bootstyle = 'warning', variable = var_hapus_data, value = 'B', command = jenis_hapus)
    r_baris.place(relx = 0.02, rely = 0.05)
    r_kolom = tb.Radiobutton(ds_frame_set, text = 'Kolom', bootstyle = 'warning', variable = var_hapus_data, value = 'K', command = jenis_hapus)
    r_kolom.place(relx = 0.02, rely = 0.35)
    r_elemen = tb.Radiobutton(ds_frame_set, text = 'Elemen', bootstyle = 'warning', variable = var_hapus_data, value = 'E', command = jenis_hapus)
    r_elemen.place(relx = 0.02, rely = 0.65)
    
    stat_perubahan = 3
    btn_simpan_perubahan['state'] = 'normal'
    
def show_warning_gagal_tambah():
    messagebox.showwarning("Gagal Menambahkan", "Perbedaan Jumlah Data Spektrum dengan Data Kolom")

def show_warning_gagal_tambah_kolom():
    messagebox.showwarning("Gagal Menambahkan Kolom", "Tidak menerima kolom kosong atau tanpa karakter")

def change_data():
    global stat_perubahan, ent_baris_change, ent_kolom_change, ent_new_var, ent_var_lama
    btn_plus_col['state'] = 'disabled'
    btn_plus['state'] = 'disabled'
    btn_hapus['state'] = 'disabled'
    stat_perubahan = 4

    lbl_baris_change = tb.Label(ds_frame_set, text= "Baris       :", bootstyle = "info", font = ("Verdana", 9))
    lbl_baris_change.place(relx = 0.02, rely = 0.15)
    lbl_kolom_change = tb.Label(ds_frame_set, text= "Kolom     :", bootstyle = "info", font = ("Verdana", 9))
    lbl_kolom_change.place(relx = 0.02, rely = 0.6)

    lbl_var_lama = tb.Label(ds_frame_set, text= "Var Lama    :", bootstyle = "info", font = ("Verdana", 9))
    lbl_var_lama.place(relx = 0.45, rely = 0.15)
    lbl_new_var = tb.Label(ds_frame_set, text= "Var Baru     :", bootstyle = "info", font = ("Verdana", 9))
    lbl_new_var.place(relx = 0.45, rely = 0.55)


    ent_baris_change = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 10, font = ("Verdana", 8))
    ent_baris_change.place(relx = 0.22, rely = 0.1)
    ent_kolom_change = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 10, font = ("Verdana", 8))
    ent_kolom_change.place(relx = 0.22, rely = 0.55)

    ent_var_lama = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 12, font = ("Verdana", 8))
    ent_var_lama.place(relx = 0.66, rely = 0.1)
    ent_new_var = tb.Entry(ds_frame_set, bootstyle = "info", state = 'disabled', width = 12, font = ("Verdana", 8))
    ent_new_var.place(relx = 0.66, rely = 0.55)

    btn_simpan_perubahan['state'] = 'normal'

def simpan_perubahan():
    global df, ls_val, file_contents, stat_perubahan, ent_baris, ent_kolom, var_hapus_data, ent_tambah_nama_kolom, ent_tambah_kolom_idx, var_tambah_spektrum, numeric_indices, string_indices, x_data_plot, kolom_string, kolom_numerik, y_data_plot, ent_new_var, ent_kolom_change, ent_baris_change
    
    if stat_perubahan == 1: #and btn_plus_col['state'] == 'disabled' and btn_hapus['state'] == 'disabled':
        if var_tambah_spektrum.get() == True: # Jika Spektrum Ikut Ditambahkan
            data_lambda = np.round(x_data_plot, constant_)
            idx_data_xy = np.where(np.isin(data_lambda, kolom_numerik))[0]
            data_spektrum = y_data_plot[idx_data_xy]
            if len(idx_data_xy) == len(kolom_numerik): # Jika panjang data yang ada dikolom jumlahnya sama dengan panjang data spektrum
                var_nilai_presisi = file_contents[13].split(" ")
                if var_jenis_data.get() == 'I':
                    
                    data_spektrum = y_data_plot[idx_data_xy]
                    new_row = pd.Series(np.nan, index=df.columns) # membuat satu baris dataframe baru yang berisi nan
                    for i, v in zip(numeric_indices, data_spektrum): # membuat barisan dataframe ini berganti menjadi nilai intensitas
                        new_row.iloc[i] = round(v, int(var_nilai_presisi[1]))

                    for i, v in zip(string_indices, ls_val): # menambahkan nilai kolom lain
                        if v.strip() and not v.isspace():
                            new_row.iloc[i] = v

                    df = df.append(new_row, ignore_index=True)
                        

                if var_jenis_data.get() == 'A':
                    pass
            
            if len(idx_data_xy) != len(kolom_numerik):
                show_warning_gagal_tambah()
                pass

            
        if var_tambah_spektrum.get() == False: # Jika Spektrum Tidak Ikut Ditambahkan
            
            new_row = pd.Series(np.nan, index=df.columns) # membuat satu baris dataframe baru yang berisi nan
            for i, v in zip(string_indices, ls_val): # menambahkan nilai kolom lain
                if v.strip() and not v.isspace():
                    new_row.iloc[i] = v
            df = df.append(new_row, ignore_index=True)

    if stat_perubahan == 2:
        new_column_values = []
        new_column_name = ent_tambah_nama_kolom.get()
        try :
            col_idx = float(ent_tambah_kolom_idx.get())
            
        except ValueError:
            col_idx = ent_tambah_kolom_idx.get()
        try:
            insert_index = np.where(df.columns == col_idx)[0][0]   # Lokasi di tengah DataFrame

            if new_column_name.strip() and not new_column_name.isspace():
                if len(new_column_values) != df.shape[0]:
                    new_column_values = [np.nan]*df.shape[0]
                try:
                    col_name = float(new_column_name)
                    df.insert(int(insert_index), col_name, new_column_values)
                except ValueError:
                    df.insert(int(insert_index), new_column_name, new_column_values)
            
            else :
                show_warning_gagal_tambah_kolom()
                pass
        except IndexError:
            pass

    if stat_perubahan == 3:
        if var_hapus_data.get() == 'B':
            df = df.drop(int(ent_baris.get()))

        if var_hapus_data.get() == 'K':
            try : 
                var_kolom = float(ent_kolom.get())
            except ValueError:
                var_kolom = str(ent_kolom.get())
            df = df.drop(var_kolom, axis = 1)

        if var_hapus_data.get() == 'E':
            try : 
                var_kolom = float(ent_kolom.get())
            except ValueError:
                var_kolom = str(ent_kolom.get())
                     
            df.at[int(ent_baris.get()), var_kolom] = np.nan

    if stat_perubahan == 4:
        try : 
            var_baru = float(ent_new_var.get())
        except ValueError:
            var_baru = str(ent_new_var.get())
        
        try :
            nama_kolom_ch = float(ent_kolom_change.get())
        except ValueError:
            nama_kolom_ch = ent_kolom_change.get()
        df.loc[int(ent_baris_change.get()), nama_kolom_ch] = var_baru
        
    if stat_perubahan == 0:
        pass


    btn_plus['state'] = 'normal'
    btn_plus_col['state'] = 'normal'
    btn_hapus['state'] = 'normal'
    btn_change['state'] = 'normal'
    clear_ds_frame_set()
    tampil_data()
    btn_simpan_perubahan['state'] = 'disabled'

    stat_perubahan = 0
    

stat_perubahan = 0
ds_frame = tb.LabelFrame(ctr_frame, text = 'Pengaturan Data', bootstyle = 'danger')
ds_frame.place(height = 0.53*(0.5*h), width = 0.9*(0.4*w), rely = 0.44, relx = 0.05)

btn_plus = tb.Button(ds_frame, text = 'Data', image= icon_plus, compound = tb.LEFT, bootstyle = 'light-outline', state = 'disabled', command = tambah_data, width = 9)
btn_plus.place(relx= 0.05, rely = 0.02)

btn_plus_col = tb.Button(ds_frame, text = 'Kolom', image= icon_plus, compound = tb.LEFT, bootstyle = 'light-outline', state = 'disabled', command = tambah_kolom, width = 9)
btn_plus_col.place(relx= 0.41, rely = 0.02)

btn_hapus = tb.Button(ds_frame, image= icon_hapus, bootstyle = 'light-outline', state = 'disabled', command = hapus_data, width = 9)
btn_hapus.place(relx= 0.77, rely = 0.02)

btn_change = tb.Button(ds_frame, image= icon_change, bootstyle = 'light-outline', state = 'disabled', command = change_data, width = 9)
btn_change.place(relx= 0.87, rely = 0.02)

btn_simpan_perubahan = tb.Button(ds_frame, text = 'Simpan Perubahan', bootstyle = 'light-outline', state = 'disabled', command = simpan_perubahan, width = 50)
btn_simpan_perubahan.place(relx= 0.1, rely = 0.82)

ds_frame_set = tb.LabelFrame(ds_frame, bootstyle = 'danger')
ds_frame_set.place(height = 0.55*(0.5*(0.5*h)), width = 0.94*(0.9*(0.4*w)), rely = 0.19, relx = 0.025)

 
### === Camera === ###
try:
    cap = cv2.VideoCapture(int(file_contents[7]))

except ValueError:
    cap = cv2.VideoCapture(file_contents[7])

w_cam, h_cam = 1280, 720    #rescale menjadi setengahnya 640 x 360
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_cam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_cam)
canvas_cam = tb.Canvas(cam_frame, width=int(w_cam*0.5), height=int(h_cam*0.5))
canvas_cam.place(relx = 0.2, rely = 0)

# Memanggil fungsi untuk memperbarui frame kamera
ROI = []

def update_box():
    global ROI_, ROI, img_luv, frame, ret
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_luv = cv2.cvtColor(frame, cv2.COLOR_RGB2Luv)[:,:,0]
        
        scaled_frame = cv2.resize(frame, (640, 360))
        photo = ImageTk.PhotoImage(image=Image.fromarray(scaled_frame))
        canvas_cam.delete('all')
        canvas_cam.create_image(0, 0, image=photo, anchor=tb.NW)
        canvas_cam.photo = photo
    
    try:
        # ukuran untuk tampilan perhitungan termasuk penampilan grafik
        X_percent = int(int(val_X)*w_cam/100)
        Y_percent = int(int(val_Y)*h_cam/100)
        hor = int(int(val_hor)*(w_cam-X_percent)/100)
        ver = int(int(val_ver)*(h_cam-Y_percent)/100)

        # ukuran untuk tampilan di aplikasi
        X_percent_ = int(int(val_X)*640/100) 
        Y_percent_ = int(int(val_Y)*360/100)
        hor_ = int(int(val_hor)*(640-X_percent_)/100)
        ver_ = int(int(val_ver)*(360-Y_percent_)/100)
        
        if len(ROI) > 9:
            ROI = []
        ROI_ = np.mean(img_luv[Y_percent: Y_percent+ver, X_percent:X_percent+hor], 0)
        if len(ROI) <= 9:
            ROI.append(ROI_)
        
        #print(Y_percent, Y_percent+ver, X_percent, X_percent+hor, np.shape(img_luv))
    except ValueError:
        pass
    
    canvas_cam.create_rectangle(X_percent_, Y_percent_, X_percent_+hor_, Y_percent_+ver_, outline = 'orange', width=3, tags = 'rectangle')
    canvas_cam.tag_raise('rectangle')  
    wd.after(1, update_box)
    
bounding_box = [value for value in file_contents[1].split()]
val_X, val_hor, val_Y, val_ver = bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]


def apply_change(event=None):
    global val_X, val_hor, val_Y, val_ver, file_contents, x_data_new
    temp_bound_box = [e_bc_xinit.get(), e_bc_hor.get(), e_bc_yinit.get(), e_bc_vert.get()]
    for idx, val in enumerate(temp_bound_box):
        if val.strip() and not val.isspace():
            if idx == 0:
                try :
                    val_X = str(int(e_bc_xinit.get()))
                except ValueError:
                    pass
            if idx == 1:
                try :
                    val_hor = str(int(e_bc_hor.get()))
                except ValueError:
                    pass
            if idx == 2:
                try :
                    val_Y = str(int(e_bc_yinit.get()))
                except ValueError:
                    pass
            if idx == 3:
                try :
                    val_ver = str(int(e_bc_vert.get()))
                except ValueError:
                    pass
    file_contents[1] = val_X + " " + val_hor + " " + val_Y  + " " + val_ver + "\n"

    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'w') as file:
        file.writelines(file_contents)

    with open(os.path.join(file_path_general,'pengaturan_dasar.txt').replace('\\', '/'), 'r') as file:
    # Baca seluruh isi file dan simpan dalam variabel
        file_contents = file.readlines()

      

update_box()



y_init = tb.Label(cam_frame, text= "Y awal", bootstyle = "info", font = ("Verdana", 10))
y_init.place(relx = 0.01, rely = 0.02)
e_bc_yinit = tb.Entry(cam_frame, bootstyle = "info", width = 10, font = ("Helvetica"))
e_bc_yinit.place(relx = 0.01, rely = 0.1)
e_bc_yinit.bind("<KeyRelease>", apply_change)

y_final = tb.Label(cam_frame, text= "Vertikal", bootstyle = "info", font = ("Verdana", 10))
y_final.place(relx = 0.01, rely = 0.22)
e_bc_vert = tb.Entry(cam_frame, bootstyle = "info", width = 10, font = ("Helvetica"))
e_bc_vert.place(relx = 0.01, rely = 0.3)
e_bc_vert.bind("<KeyRelease>", apply_change)

x_init = tb.Label(cam_frame, text= "X awal", bootstyle = "info", font = ("Verdana", 10))
x_init.place(relx = 0.01, rely = 0.42)
e_bc_xinit = tb.Entry(cam_frame, bootstyle = "info", width = 10, font = ("Helvetica"))
e_bc_xinit.place(relx = 0.01, rely = 0.5)
e_bc_xinit.bind("<KeyRelease>", apply_change)

x_final = tb.Label(cam_frame, text= "Horizontal", bootstyle = "info", font = ("Verdana", 10))
x_final.place(relx = 0.01, rely = 0.62)
e_bc_hor = tb.Entry(cam_frame, bootstyle = "info", width = 10, font = ("Helvetica"))
e_bc_hor.place(relx = 0.01, rely = 0.7)
e_bc_hor.bind("<KeyRelease>", apply_change)

def save_cam():
    global frame, ret
    if ret:
        file_path_graph = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png;*.jpeg;*.pdf;*.jpg;*.svg")])
        #print(frame)cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(file_path_graph, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    else : 
        messagebox.showwarning("Kamera Tidak Terhubung", "Tidak Dapat Mengambil Gambar, Cek Kamera!")

btn_save_pict = tb.Button(cam_frame, image= icon_sv_pict, bootstyle = 'info-outline', state = 'normal', command = save_cam, width = 9)
btn_save_pict.place(relx= 0.05, rely = 0.85)


### === Notebook === ####
def find_nearest(x_array, x_value):
    idx = (np.abs(x_array - x_value)).argmin()
    return x_array[idx], idx

def on_click(event, x_data, y_data):
    global x_nearest, y_nearest
    x = event.xdata
    y = event.ydata
    if x is not None and y is not None:
        x_nearest, idx = find_nearest(x_data, x)
        y_nearest = y_data[idx]

        if var1.get() is False and btn_kalib['text'] == 'Simpan': 
            trim_point1['state'] = 'normal'
        if var1.get() is True and btn_kalib['text'] == 'Simpan': 
            trim_point2['state'] = 'normal'
    


def replace_nan(y_t):
    invalid_indices = np.where(y_t <= 0)[0]

    for idx in invalid_indices:
        # Mencari tetangga terdekat yang bukan nol atau negatif
        left_idx = idx - 1
        right_idx = idx + 1

        # Cari nilai yang valid di sebelah kiri
        while left_idx >= 0 and y_t[left_idx] <= 0:
            left_idx -= 1

        # Cari nilai yang valid di sebelah kanan
        while right_idx < len(y_t) and y_t[right_idx] <= 0:
            right_idx += 1

        # Tetapkan nilai baru dari tetangga terdekat yang valid
        if left_idx >= 0 and right_idx < len(y_t):
            if idx - left_idx <= right_idx - idx:
                y_t[idx] = y_t[left_idx]
            else:
                y_t[idx] = y_t[right_idx]
        elif left_idx >= 0:
            y_t[idx] = y_t[left_idx]
        elif right_idx < len(y_t):
            y_t[idx] = y_t[right_idx]
    return y_t


def graph():
    global ROI_, ROI, fig, y_data_plot, x_data_plot, constant_FILE_REF, val_file_ref, col_file_ref, default_title, default_xlabel, default_ylabel, default_y_max, default_warna_grafik, default_warna_tepi, default_x_nbins, default_y_nbins, var_status_Amb, var_status_A
    x_data_plot = np.linspace(x_limit[0], x_limit[1], len(ROI_))
    if var_status_Amb.get() == True:
        data_x_amb = np.round(x_data_plot, constant_FILE_AMB)
        idx_data_xy_FILE_AMB = np.where(np.isin(data_x_amb, col_file_amb))
        
        if len(data_x_amb) == len(idx_data_xy_FILE_AMB[0]): # Jika panjang data x skrg sama panjang dengan data x pada file ambient (lingkungan)
            if var_status_A.get() == False:
                if int(file_contents[17]) == 1:
                    try :
                        y_data_plot = savgol_filter(replace_nan(np.mean(ROI, 0).astype(np.float64) - val_file_amb), window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1]))
                    except ValueError:
                        messagebox.showwarning("Kesalahan Parameter SavGol", "Orde Polinomial melebihi panjang jendela")
                        var_status_savgol.set(False)
                        y_data_plot = replace_nan(np.mean(ROI, 0).astype(np.float64) - val_file_amb)

                if int(file_contents[17]) == 0:
                    y_data_plot = replace_nan(np.mean(ROI, 0).astype(np.float64) - val_file_amb)
                
            if var_status_A.get() == True:
                data_x_abs = np.round(x_data_plot, constant_FILE_REF)
                idx_data_xy_FILE_REF = np.where(np.isin(data_x_abs, col_file_ref))
                if len(idx_data_xy_FILE_REF[0]) != len(data_x_abs):
                    messagebox.showwarning("File Referensi Absorbsi Berbeda", "Ganti atau Buat file referensi absorbsi baru!")
                    var_status_A.set(False)
                if len(idx_data_xy_FILE_REF[0]) == len(data_x_abs):
                    if int(file_contents[17]) == 1:
                        try :
                            Io = savgol_filter(val_file_ref-val_file_amb, window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1]))
                            It = np.minimum(savgol_filter(replace_nan(np.mean(ROI, 0).astype(np.float64)-val_file_amb), window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1])), Io)
                            y_data_plot = np.log10(Io/It)
                        except ValueError:
                            messagebox.showwarning("Kesalahan Parameter SavGol", "Orde Polinomial melebihi panjang jendela")
                            var_status_savgol.set(False)
                            y_data_plot = np.log10((val_file_ref-val_file_amb)/np.minimum(replace_nan(np.mean(ROI, 0).astype(np.float64)-val_file_amb), (val_file_ref-val_file_amb)))

                    if int(file_contents[17]) == 0:
                        y_data_plot = np.log10((val_file_ref-val_file_amb)/np.minimum(replace_nan(np.mean(ROI, 0).astype(np.float64)-val_file_amb), (val_file_ref-val_file_amb)))
        
        if len(data_x_amb) != len(idx_data_xy_FILE_AMB[0]):
            messagebox.showwarning("File Referensi Lingkungan Berbeda", "Ganti atau Buat file referensi lingkungan baru!")
            var_status_Amb.set(False)
                
    if var_status_Amb.get() == False : 
        if var_status_A.get() == False:
            if int(file_contents[17]) == 1:
                try :
                    y_data_plot = savgol_filter(replace_nan(np.mean(ROI, 0).astype(np.float64)), window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1]))
                except ValueError:
                    messagebox.showwarning("Kesalahan Parameter SavGol", "Orde Polinomial melebihi panjang jendela")
                    var_status_savgol.set(False)
                    y_data_plot = replace_nan(np.mean(ROI, 0).astype(np.float64))
            if int(file_contents[17]) == 0:
                y_data_plot = replace_nan(np.mean(ROI, 0).astype(np.float64))                     
            
        if var_status_A.get() == True:
            data_x_abs = np.round(x_data_plot, constant_FILE_REF)
            idx_data_xy_FILE_REF = np.where(np.isin(data_x_abs, col_file_ref))
            if len(idx_data_xy_FILE_REF[0]) != len(data_x_abs):
                messagebox.showwarning("File Referensi Absorbsi Berbeda", "Ganti atau Buat file referensi absorbsi baru!")
                var_status_A.set(False)
            if len(idx_data_xy_FILE_REF[0]) == len(data_x_abs):

                if int(file_contents[17]) == 1:
                    try :
                        Io = savgol_filter(val_file_ref, window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1]))
                        It = np.minimum(savgol_filter(replace_nan(np.mean(ROI, 0).astype(np.float64)), window_length=int(file_contents[15].split(" ")[0]), polyorder=int(file_contents[15].split(" ")[1])), Io)
                        y_data_plot = np.log10(Io/It)
                    except ValueError:
                        messagebox.showwarning("Kesalahan Parameter SavGol", "Orde Polinomial melebihi panjang jendela")
                        var_status_savgol.set(False)
                        y_data_plot = np.log10(val_file_ref/np.minimum(replace_nan(np.mean(ROI, 0).astype(np.float64)), val_file_ref))
                if int(file_contents[17]) == 0:
                    y_data_plot = np.log10(val_file_ref/np.minimum(replace_nan(np.mean(ROI, 0).astype(np.float64)), val_file_ref))
            
    ax.clear()
    ax.plot(x_data_plot, y_data_plot, color = default_warna_grafik)
    ax.set_title(default_title, color = default_warna_tepi, fontsize = 11)
    ax.set_xlabel(default_xlabel, color = default_warna_tepi, fontsize = 11)
    ax.set_ylabel(default_ylabel, color = default_warna_tepi, fontsize = 11)
    ax.spines['bottom'].set_color(default_warna_tepi)  
    ax.spines['left'].set_color(default_warna_tepi)   
    ax.spines['top'].set_color(default_warna_tepi)   
    ax.spines['right'].set_color(default_warna_tepi)
    ax.tick_params(axis='x', colors=default_warna_tepi)  
    ax.tick_params(axis='y', colors=default_warna_tepi)
    ax.set_ylim(0, default_y_max)
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=default_x_nbins))
    
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=default_y_nbins))
    ax.grid(color='gray', linestyle='-.', linewidth=0.5)
    ax.set_xlim(x_data_plot[0], x_data_plot[-1])
    fig.tight_layout()
    canvas_graph.mpl_connect('button_press_event', lambda event: on_click(event, x_data_plot, y_data_plot))

    canvas_graph.draw()




nb = tb.Notebook(wd)

nb_graph_frame = tb.Frame(nb, height = 0.4*h, width = 0.96*w)
nb_num_frame = tb.Frame(nb, height = 0.4*h, width = 0.96*w)

nb.add(nb_graph_frame, text = "Grafik")

fig = Figure(figsize = (9.8, 2.9))#, facecolor = #'#222222')
fig.patch.set_facecolor('none')
ax = fig.add_subplot()
default_title = 'Intensitas'
default_xlabel = 'Panjang Gelombang (nm)'
default_ylabel = 'Nilai Digital'
default_y_max = 255
default_warna_grafik = 'dimgrey'
default_warna_tepi = 'orange'
default_x_nbins = 15
default_y_nbins = 7
x_limit = [float(value) for value in file_contents[3].split()]
canvas_graph = FigureCanvasTkAgg(fig, master=nb_graph_frame)
canvas_graph.get_tk_widget().place(relx = 0.2, rely = 0)


def toggle_status_A(): # untuk mengubah variabel-variabel dalam grafik dan menambah variabel untuk  abs
    global file_contents, val_file_ref, col_file_ref, constant_FILE_REF

    try : 
        file_ref = pd.read_excel(file_contents[9][:-1])
        val_file_ref = file_ref.iloc[0].values.astype(np.float64)
        col_file_ref = file_ref.columns
        idx_random_FILE_REF = np.random.randint(0, len(col_file_ref), 5)
        panjang_dibelakang_koma_FILE_REF = [len(col_file_ref[idx].astype(str).split('.')[1]) for idx in idx_random_FILE_REF]
        constant_FILE_REF = np.max(panjang_dibelakang_koma_FILE_REF)

    except FileNotFoundError:
        messagebox.showwarning("File Referensi tidak ditemukan", "Tambah atau ganti File Referensi baru!")
        var_status_A.set(False)

    except NameError:
        messagebox.showwarning("File Referensi tidak ditemukan", "Tambah atau ganti File Referensi baru!")
        var_status_A.set(False)

def toggle_status_amb():
    global file_contents, val_file_amb, col_file_amb, constant_FILE_AMB
    try:
        file_amb = pd.read_excel(file_contents[11][:-1])
        val_file_amb = file_amb.iloc[0].values.astype(np.float64)
        col_file_amb = file_amb.columns
        idx_random_FILE_AMB = np.random.randint(0, len(col_file_amb), 5)
        panjang_dibelakang_koma_FILE_AMB = [len(col_file_amb[idx].astype(str).split('.')[1]) for idx in idx_random_FILE_AMB]
        constant_FILE_AMB = np.max(panjang_dibelakang_koma_FILE_AMB)
    except FileNotFoundError:
        messagebox.showwarning("File Intensitas Ambient tidak ditemukan", "Tambah atau ganti File Referensi baru!")
        var_status_Amb.set(False)
    except NameError:
        messagebox.showwarning("File Intensitas Ambient tidak ditemukan", "Tambah atau ganti File Referensi baru!")
        var_status_Amb.set(False)
        
        

def apply_graph():
    global default_title, default_xlabel, default_ylabel, default_y_max, default_warna_grafik, default_warna_tepi, default_x_nbins, default_y_nbins

    fitur_graph = [ent_judul_grafik.get(), ent_label_x.get(), ent_label_y.get(), ent_y_max.get(), cb_color_plt.get(), cb_color_tepi_plt.get(), sb_x_nbins.get(), sb_y_nbins.get()]
    for idx, val in enumerate(fitur_graph):
        if val.strip() and not val.isspace():
            if idx == 0:
                default_title = val
            if idx == 1:
                default_xlabel = val
            if idx == 2:
                default_ylabel = val
            if idx == 3:
                try : 
                    default_y_max = int(val)
                except ValueError:
                    pass
            if idx == 4:
                default_warna_grafik = val
            if idx == 5:
                default_warna_tepi = val
            if idx == 6:
                try : 
                    default_x_nbins = int(val)
                except ValueError:
                    pass
            if idx == 7:
                try : 
                    default_y_nbins = int(val)
                except ValueError:
                    pass


def save_graph():
    global fig,file_path_general
    file_path_graph = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png;*.jpeg;*.pdf;*.jpg;*.svg")])
    fig.savefig(file_path_graph, transparent=True)


Judul_grafik = tb.Label(nb_graph_frame, text= "Judul Grafik", bootstyle = "info", font = ("Verdana", 9))
Judul_grafik.place(relx = 0.01, rely = 0.167)

ent_judul_grafik = tb.Entry(nb_graph_frame, bootstyle = "info", state = 'normal', width = 15, font = ("Verdana", 8))
ent_judul_grafik.place(relx = 0.08, rely = 0.145)

label_x_grafik = tb.Label(nb_graph_frame, text= "Label X", bootstyle = "info", font = ("Verdana", 9))
label_x_grafik.place(relx = 0.01, rely = 0.267)

ent_label_x = tb.Entry(nb_graph_frame, bootstyle = "info", state = 'normal', width = 15, font = ("Verdana", 8))
ent_label_x.place(relx = 0.08, rely = 0.245)

label_y_grafik = tb.Label(nb_graph_frame, text= "Label Y", bootstyle = "info", font = ("Verdana", 9))
label_y_grafik.place(relx = 0.01, rely = 0.367)

ent_label_y = tb.Entry(nb_graph_frame, bootstyle = "info", state = 'normal', width = 15, font = ("Verdana", 8))
ent_label_y.place(relx = 0.08, rely = 0.345)

nilai_y_max = tb.Label(nb_graph_frame, text= "Nilai Y Maks", bootstyle = "info", font = ("Verdana", 9))
nilai_y_max.place(relx = 0.01, rely = 0.467)

ent_y_max = tb.Entry(nb_graph_frame, bootstyle = "info", state = 'normal', width = 15, font = ("Verdana", 8))
ent_y_max.place(relx = 0.08, rely = 0.45)

warna_grafik = tb.Label(nb_graph_frame, text= "Warna Grafik", bootstyle = "info", font = ("Verdana", 9))
warna_grafik.place(relx = 0.01, rely = 0.567)

color_plt = ['black', 'dimgrey', 'brown', 'red', 'darkorange', 'orange', 'olive', 'yellow', 'gold', 'green', 'darkcyan', 'steelblue', 'blue', 'indigo', 'darkviolet', 'purple', 'crimson', 'deeppink']
cb_color_plt = tb.Combobox(nb_graph_frame, values = color_plt, bootstyle = 'warning', width = 9)
cb_color_plt.place(relx = 0.08, rely = 0.55)

warna_tepi_grafik = tb.Label(nb_graph_frame, text= "Warna Tepi", bootstyle = "info", font = ("Verdana", 9))
warna_tepi_grafik.place(relx = 0.01, rely = 0.677)

cb_color_tepi_plt = tb.Combobox(nb_graph_frame, values = color_plt, bootstyle = 'warning', width = 9)
cb_color_tepi_plt.place(relx = 0.08, rely = 0.66)

x_nbins = tb.Label(nb_graph_frame, text= "nX", bootstyle = "info", font = ("Verdana", 9))
x_nbins.place(relx = 0.01, rely = 0.787)

sb_x_nbins = tb.Spinbox(nb_graph_frame, bootstyle = 'warning', from_=5, to=18, width = 6)
sb_x_nbins.place(relx= 0.03, rely = 0.77)

x_nbins = tb.Label(nb_graph_frame, text= "nY", bootstyle = "info", font = ("Verdana", 9))
x_nbins.place(relx = 0.1, rely = 0.787)

sb_y_nbins = tb.Spinbox(nb_graph_frame, bootstyle = 'warning', from_=3, to=10, width = 6)
sb_y_nbins.place(relx= 0.12, rely = 0.77)

btn_terapkan = tb.Button(nb_graph_frame, image= icon_apply, bootstyle = 'light-outline', state = 'normal', command = apply_graph, width = 9)
btn_terapkan.place(relx= 0.01, rely = 0.89)

btn_save_graph = tb.Button(nb_graph_frame, image= icon_sv_graph, bootstyle = 'light-outline', state = 'normal', command = save_graph, width = 9)
btn_save_graph.place(relx= 0.05, rely = 0.89)

var_status_A = BooleanVar()
var_status_A.set(False)

var_status_Amb = BooleanVar()
var_status_Amb.set(False)

cb_status_A = tb.Checkbutton(nb_graph_frame, bootstyle = 'warning-round_toggle', text = "Absorbsi", variable = var_status_A, state= 'normal', command = toggle_status_A)
cb_status_A.place(relx = 0.011, rely = 0.06)

cb_status_Amb = tb.Checkbutton(nb_graph_frame, bootstyle = 'warning-round_toggle', text = "Lingkungan", variable = var_status_Amb, state= 'normal', command = toggle_status_amb)
cb_status_Amb.place(relx = 0.09, rely = 0.06)

def continuous_update():
    while True:
        if len(ROI) == 8:
            graph()
        time.sleep(0.001)


thread = threading.Thread(target=continuous_update)
thread.daemon = True  # Mengatur thread agar berhenti saat aplikasi ditutup
thread.start()

nb.add(nb_num_frame, text = "Data")
nb.pack(expand=0, fill = 'both', padx = 10, pady = 10, side = "bottom")

data = tb.Treeview(nb_num_frame)
data.place(relheight=1, relwidth=1) # atur height dan width menjadi 1 atau 100% dalam mainframe
yd_scroll = tb.Scrollbar(nb_num_frame, orient = "vertical", bootstyle="danger-round", command = data.yview) # perintah/command berarti mengupdate view sb y dari widget 
xd_scroll = tb.Scrollbar(nb_num_frame, orient = "horizontal", bootstyle="danger-round", command = data.xview) # perintah/command berarti mengupdate view sb x dari widget 
data.configure(xscrollcommand=xd_scroll.set, yscrollcommand=yd_scroll.set)
xd_scroll.pack(side="bottom", fill="x")
yd_scroll.pack(side="right", fill="y")


wd.protocol("WM_DELETE_WINDOW", on_closing)

wd.mainloop()