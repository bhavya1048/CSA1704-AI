import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_processing import analyze_image
from rule_engine import diagnose

class CropDiseaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Disease Expert System")
        self.root.geometry("900x700")
        self.root.configure(bg="#eef4ea")
        self.image_path = None
        self.photo = None

        tk.Label(root, text="CROP DISEASE EXPERT SYSTEM",
                 font=("Arial", 22, "bold"), bg="#eef4ea").pack(pady=15)

        top = tk.Frame(root, bg="#eef4ea")
        top.pack(pady=5)

        tk.Button(top, text="Select Leaf Image", command=self.select_image,
                  font=("Arial", 12, "bold"), width=18).grid(row=0, column=0, padx=10)

        tk.Button(top, text="Analyze Image", command=self.analyze,
                  font=("Arial", 12, "bold"), width=18).grid(row=0, column=1, padx=10)

        self.image_label = tk.Label(root, text="No image selected",
                                    width=60, height=18, bg="white")
        self.image_label.pack(pady=15)

        self.result = tk.Text(root, height=15, width=95,
                              font=("Consolas", 11))
        self.result.pack(pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(
            title="Select Leaf Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("All Files", "*.*")
            ]
        )
        if not path:
            return

        self.image_path = path

        img = Image.open(path)
        img.thumbnail((500, 330))
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo, text="")

        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, "Image selected successfully.\nClick 'Analyze Image'.")

    def analyze(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please select a leaf image first.")
            return

        try:
            features, facts = analyze_image(self.image_path)
            disease, cf, fired_rules = diagnose(facts)

            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, "===== DIAGNOSIS RESULT =====\n\n")
            self.result.insert(tk.END, f"Disease       : {disease}\n")
            self.result.insert(tk.END, f"Certainty     : {cf:.2f} ({cf*100:.1f}%)\n\n")

            self.result.insert(tk.END, "===== EXTRACTED FEATURES =====\n")
            for key, value in features.items():
                self.result.insert(tk.END, f"{key:<22}: {value}\n")

            self.result.insert(tk.END, "\n===== SYMBOLIC FACTS =====\n")
            for key, value in facts.items():
                self.result.insert(tk.END, f"{key:<22}: {value}\n")

            self.result.insert(tk.END, "\n===== FIRED RULES =====\n")
            if fired_rules:
                for rule in fired_rules:
                    self.result.insert(tk.END, f"✓ {rule}\n")
            else:
                self.result.insert(tk.END, "No disease rule matched strongly.\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
app = CropDiseaseApp(root)
root.mainloop()
