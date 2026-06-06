import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog
import os

BG_COLOR = "#2C003E"
BTN_COLOR = "#D100D1"
BTN_HOVER = "#E754E7"
TEXT_COLOR = "#FFFFFF"
FUNKY_FONT='Juice ITC'
NORMAL_FONT='Segoe UI'
last_saved_path = None


def get_max_loss(row):
    comment = row.get('Comment', None)
    if comment is not None and str(comment).strip() not in ('', 'nan', 'None', 'NaN'):
        return comment
    return row['MaxLoss%']


def merge_ghost_by_single_file(df, ghost_collar_length):
    merged_rows = []
    i = 0
    while i < len(df):
        current = df.iloc[i]

        j = i
        merged = False
        while j < len(df) - 1:
            next_row = df.iloc[j + 1]
            collar_len = round(next_row['Top'] - df.iloc[j]['Bottom'], 2)

            if collar_len >= ghost_collar_length:
                j += 1
                merged = True
            else:
                break

        if merged:
            merge_group = df.iloc[i:j+1]
            best_row = merge_group.loc[merge_group['MaxLoss%'].idxmax()]
            max_loss_val = get_max_loss(best_row)

            merged_rows.append({
                'Top': merge_group.iloc[0]['Top'],
                'Bottom': merge_group.iloc[-1]['Bottom'],
                'Length': merge_group.iloc[-1]['Bottom'] - merge_group.iloc[0]['Top'],
                'TNom': merge_group.iloc[0]['TNom'],
                'TMin': merge_group['TMin'].min(),
                'DptMxLos': best_row['DptMxLos'],
                'MaxLoss%': max_loss_val,
                'Source': 'merged (ghost collar chain)'
            })
            i = j + 1
        else:
            max_loss_val = get_max_loss(current)
            merged_rows.append({
                'Top': current['Top'],
                'Bottom': current['Bottom'],
                'Length': current['Bottom'] - current['Top'],
                'TNom': current['TNom'],
                'TMin': current['TMin'],
                'DptMxLos': current['DptMxLos'],
                'MaxLoss%': max_loss_val,
                'Source': 'original'
            })
            i += 1

    column_order = ['Top', 'Bottom', 'Length', 'TNom', 'TMin', 'DptMxLos', 'MaxLoss%', 'Source']
    return pd.DataFrame(merged_rows)[column_order]

def load_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return None, None
    df = pd.read_csv(file_path, skiprows=2)
    df.columns = df.columns.str.strip()
    df = df.sort_values(by='Top').reset_index(drop=True)
    return df, file_path

def save_to_excel(df, original_filename):
    out_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        initialfile=f"merged_{os.path.basename(original_filename).replace('.csv', '')}.xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )
    if out_path:
        df.to_excel(out_path, index=False)
        return out_path
    return None


def run_merge():
    df, source = load_csv_file()
    if df is None:
        status_label.config(text="No file selected.", fg="white")
        return

    try:
        ghost_length_input = float(ghost_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for ghost collar length.")
        status_label.config(text="❌ Invalid collar length input.", fg="red")
        return

    try:
        merged = merge_ghost_by_single_file(df, ghost_collar_length=ghost_length_input)
        saved_path = save_to_excel(merged, source)
        global last_saved_path
        last_saved_path = saved_path
        if saved_path:
            messagebox.showinfo("✅ Success", f"Merged file saved to:\n{saved_path}")
            status_label.config(text="✅ Success: File saved.", fg="green")
        else:
            status_label.config(text="No output path returned.", fg="orange")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to process file:\n{str(e)}")
        status_label.config(text="❌ Error occurred.", fg="red")

def validate_numeric_input(new_value):
    if new_value == "":
        return True  # allow empty string for now (e.g., during typing)
    try:
        return float(new_value) > 0
    except ValueError:
        return False



def open_output_folder():
    if last_saved_path:
        folder = os.path.dirname(last_saved_path)
        try:
            if os.name == 'nt':
                os.startfile(folder)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open folder:\n{e}")
    else:
        messagebox.showinfo("No File", "No output file has been saved yet.")
# --- Main UI ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ghost Collar Merger")
    root.geometry("480x280")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # Optional icon (must be .ico format)
    # root.iconbitmap("icon.ico")

    header = tk.Label(
        root, 
        text="Ghost Collar Merger 👻",
        font=(FUNKY_FONT, 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR 
    )
    header.pack(pady=(20, 5))

    
    vcmd = (root.register(validate_numeric_input), '%P')

    input_frame = tk.Frame(root, bg=BG_COLOR)
    input_frame.pack(pady=(0, 20))

    sublabel = tk.Label(
        input_frame,
        text="Merge Ghost Collars (length ft)   >=",
        font=(NORMAL_FONT, 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    sublabel.pack(side="left", padx=(0, 10))

    ghost_entry = tk.Entry(
    input_frame,
    width=5,
    font=(NORMAL_FONT, 11),
    bg="#1E1E2E",
    fg="#FFFFFF",
    insertbackground="#FFFFFF",  # white blinking cursor
    bd=1,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#555555",
    highlightcolor=BTN_COLOR,
    justify="center",
    validate="key",
    validatecommand=vcmd
    )
    ghost_entry.insert(0, "3")
    ghost_entry.pack(side="left")

    btn = tk.Button(
        root,
        text="Select CSV and Merge",
        command=run_merge,
        height=2,
        width=30,
        bg=BTN_COLOR,
        fg="white",
        font=(NORMAL_FONT, 10, "bold"),
        activebackground=BTN_HOVER,
        relief="flat",
        bd=0
    )
    btn.pack(pady=10)
    btn_open = tk.Button(
        root,
        text="Open Output Folder",
        command=open_output_folder,
        height=1,
        width=30,
        bg="#444444",
        fg="white",
        font=(NORMAL_FONT, 10),
        activebackground="#666666",
        relief="flat",
        bd=0
    )
    btn_open.pack(pady=(5, 0))


    license_label = tk.Label(
        root,
        text="MIT License © 2026 AbdullahTamer27 — see LICENSE",
        font=(NORMAL_FONT, 7),
        bg=BG_COLOR,
        fg="#666666"
    )
    license_label.pack(side="bottom", pady=(0, 4))

    # Status label
    status_label = tk.Label(
        root,
        text="",
        font=(NORMAL_FONT, 9),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    status_label.pack(side="bottom", pady=(5, 0))

    root.mainloop()
