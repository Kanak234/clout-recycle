"""
Sustainable Cloth Recyclability Analysis System
AI-Inspired Software for Sustainable Development

Author & Copyright © Kanak Prabhakar
All Rights Reserved
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import numpy as np
import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("kanak_prabhakar_cloth_ai.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    textile TEXT,
    recycle_percent REAL,
    condition TEXT,
    carbon_impact REAL,
    verdict TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ---------------- TEXTILE DATA ----------------
TEXTILE_DATA = {
    "Cotton":     {"base": 80, "carbon": 1.5},
    "Linen":      {"base": 75, "carbon": 1.4},
    "Silk":       {"base": 65, "carbon": 2.0},
    "Wool":       {"base": 70, "carbon": 2.2},
    "Polyester":  {"base": 25, "carbon": 4.5},
    "Nylon":      {"base": 20, "carbon": 4.2},
    "Acrylic":    {"base": 15, "carbon": 4.8},
    "Elastane":   {"base": 10, "carbon": 5.0},
}

# ---------------- AI IMAGE ANALYSIS ----------------
def analyze_image(image_path):
    img = Image.open(image_path).convert("L")
    pixels = np.array(img)
    brightness = pixels.mean()

    if brightness >= 170:
        return 1.0, "Excellent"
    elif brightness >= 120:
        return 0.8, "Good"
    elif brightness >= 80:
        return 0.6, "Worn"
    else:
        return 0.4, "Poor"

def ai_cloth_analysis(textile, image_path):
    base = TEXTILE_DATA[textile]["base"]
    carbon_rate = TEXTILE_DATA[textile]["carbon"]

    factor, condition = analyze_image(image_path)
    recycle_percent = base * factor
    carbon_impact = recycle_percent * carbon_rate

    if recycle_percent >= 60:
        verdict = "✅ Recyclable & Sustainable"
    elif recycle_percent >= 35:
        verdict = "⚠️ Partially Recyclable"
    else:
        verdict = "❌ Not Recommended"

    return recycle_percent, condition, carbon_impact, verdict

# ---------------- GUI FUNCTIONS ----------------
def upload_image(event=None):
    global image_path, img_display
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if image_path:
        img = Image.open(image_path).resize((220, 220))
        img_display = ImageTk.PhotoImage(img)
        image_label.config(image=img_display, text="")

def run_analysis():
    try:
        textile = textile_combo.get()
        if textile == "" or image_path == "":
            raise ValueError

        recycle, condition, carbon, verdict = ai_cloth_analysis(textile, image_path)

        result.set(
            f"AI Analysis Result\n\n"
            f"Textile Type        : {textile}\n"
            f"Cloth Condition     : {condition}\n"
            f"Recyclability       : {recycle:.2f}%\n"
            f"Carbon Impact       : {carbon:.2f}\n\n"
            f"Final Verdict       : {verdict}\n\n"
            f"AI Explanation:\n"
            f"The system analyzed cloth brightness and\n"
            f"applied sustainability rules automatically."
        )

        cur.execute("""
        INSERT INTO analysis_history
        (textile, recycle_percent, condition, carbon_impact, verdict, timestamp)
        VALUES (?,?,?,?,?,?)
        """, (
            textile,
            recycle,
            condition,
            carbon,
            verdict,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()

    except:
        messagebox.showerror(
            "Input Error",
            "Please select textile type and upload an image"
        )

# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("Sustainable Cloth AI System")
root.geometry("760x620")
root.resizable(False, False)

tk.Label(
    root,
    text="SUSTAINABLE CLOTH RECYCLABILITY ANALYSIS SYSTEM",
    font=("Arial", 15, "bold")
).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Select Textile Type").grid(row=0, column=0, padx=10)
textile_combo = ttk.Combobox(
    frame,
    values=list(TEXTILE_DATA.keys()),
    state="readonly",
    width=30
)
textile_combo.grid(row=0, column=1)

tk.Label(
    root,
    text="Upload Cloth Image (AI calculates everything automatically)",
    font=("Arial", 10, "bold")
).pack(pady=6)

image_label = tk.Label(
    root,
    text="📷 Click to Upload Image",
    width=32,
    height=12,
    relief="ridge",
    bg="#f3f3f3"
)
image_label.pack()
image_label.bind("<Button-1>", upload_image)

tk.Button(
    root,
    text="Run AI Cloth Analysis",
    command=run_analysis,
    bg="#2E7D32",
    fg="white",
    font=("Arial", 11, "bold"),
    width=25
).pack(pady=12)

result = tk.StringVar()
tk.Label(
    root,
    textvariable=result,
    justify="left",
    bg="#ECECEC",
    width=95,
    height=11,
    font=("Consolas", 10)
).pack(pady=5)

tk.Label(
    root,
    text="© Copyright Kanak Prabhakar | All Rights Reserved",
    font=("Arial", 9, "italic")
).pack(pady=6)

root.mainloop()
