import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
from customtkinter import CTkImage
import subprocess
import threading
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JaalBreak(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JaalBreak Scanner")
        self.geometry("980x750")
        self.minsize(900, 680)

        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        self.device_scan_results = []
        self.advanced_scan_results_raw = ""

        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        try:
            image_path = os.path.join(os.path.dirname(__file__), "logo.png")
            image = Image.open(image_path)
            self.logo_image = CTkImage(light_image=image, dark_image=image, size=(140, 50))
            self.sidebar_logo = ctk.CTkLabel(self.sidebar, image=self.logo_image, text="", anchor="center")
            self.sidebar_logo.pack(pady=(15, 5))
        except Exception as e:
            print(f"Logo load error: {e}")

        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=18, weight="bold"))
        self.sidebar_label.pack(pady=(10, 10))

        self.btn_scan_tab = ctk.CTkButton(self.sidebar, text="Scan", command=self.show_scan_tab)
        self.btn_scan_tab.pack(pady=10, padx=10, fill="x")

        self.btn_help_tab = ctk.CTkButton(self.sidebar, text="Help", command=self.show_help_tab)
        self.btn_help_tab.pack(pady=10, padx=10, fill="x")

        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.tabs = ctk.CTkTabview(self.container)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabs.add("Scan")
        self.tabs.add("Advanced")
        self.tabs.add("Results")

        self.build_scan_tab()
        self.build_advanced_tab()
        self.build_results_tab()
        self.tabs.set("Scan")

    def show_scan_tab(self):
        self.tabs.set("Scan")

    def show_help_tab(self):
        messagebox.showinfo("Help",
            "JaalBreak Scanner\n\n"
            "1. Scan Tab: Enter a subnet (e.g. 192.168.1.0/24).\n"
            "2. Advanced Tab: Target a host with deep scan options.\n"
            "Uses Nmap – ensure it's installed and in PATH.")

    def build_scan_tab(self):
        tab = self.tabs.tab("Scan")
        label = ctk.CTkLabel(tab, text="Network Scanner", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=15)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=10)

        self.entry_subnet = ctk.CTkEntry(frame, width=300, placeholder_text="Enter subnet (e.g. 192.168.1.0/24)")
        self.entry_subnet.pack(padx=5, pady=10)

        btn_scan = ctk.CTkButton(tab, text="Scan Network", command=self.run_network_scan)
        btn_scan.pack(pady=10)

    def build_advanced_tab(self):
        tab = self.tabs.tab("Advanced")
        label = ctk.CTkLabel(tab, text="Advanced Scan", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=15)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=10)

        self.entry_advanced_target = ctk.CTkEntry(frame, width=300, placeholder_text="Enter target IP or hostname")
        self.entry_advanced_target.pack(padx=5, pady=10)

        self.preset_menu = ctk.CTkOptionMenu(frame, values=["Custom", "Default", "Stealth", "Aggressive"], command=self.load_preset)
        self.preset_menu.set("Custom")
        self.preset_menu.pack(pady=(0, 10))

        self.safe_scan_flags = {
            "Quick Scan (-T4 -F)": ["-T4", "-F"],
            "Ping Scan (-sn)": ["-sn"],
            "Port Scan (1-1000)": ["-p", "1-1000"],
            "UDP Scan (-sU)": ["-sU"]
        }

        self.aggressive_scan_flags = {
            "Service Detection (-sV)": ["-sV"],
            "OS Detection (-O)": ["-O"],
            "Aggressive Scan (-A)": ["-A"],
            "Intense Scan (Prompt)": []
        }

        self.scan_flags = {**self.safe_scan_flags, **self.aggressive_scan_flags}
        self.scan_vars = {}
        self.scan_checkboxes = {}

        ctk.CTkLabel(frame, text="Safe Scans", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 0))
        for label_text in self.safe_scan_flags:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(frame, text=label_text, variable=var)
            chk.pack(anchor="w")
            self.scan_vars[label_text] = var
            self.scan_checkboxes[label_text] = chk

        ctk.CTkLabel(frame, text="Aggressive Scans", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 0))
        for label_text in self.aggressive_scan_flags:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(frame, text=label_text, variable=var)
            chk.pack(anchor="w")
            self.scan_vars[label_text] = var
            self.scan_checkboxes[label_text] = chk

        btn_scan = ctk.CTkButton(tab, text="Start Advanced Scan", command=self.run_advanced_scan)
        btn_scan.pack(pady=10)

    def build_results_tab(self):
        tab = self.tabs.tab("Results")
        label = ctk.CTkLabel(tab, text="Scan Results", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=15)

        self.textbox_results = ctk.CTkTextbox(tab, width=900, height=470, font=("Consolas", 12), wrap="word")
        self.textbox_results.pack(padx=15, pady=10)

        self.textbox_results.tag_config("ip", foreground="lightblue")

        self.progress_bar = ctk.CTkProgressBar(tab, width=900)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        btn_export = ctk.CTkButton(tab, text="Export to PDF", command=self.export_to_pdf)
        btn_export.pack(pady=10)

    def load_preset(self, choice):
        for label in self.scan_vars:
            self.scan_vars[label].set(False)
        if choice == "Default":
            self.scan_vars["Quick Scan (-T4 -F)"].set(True)
        elif choice == "Stealth":
            self.scan_vars["Ping Scan (-sn)"].set(True)
        elif choice == "Aggressive":
            self.scan_vars["Aggressive Scan (-A)"].set(True)
            self.scan_vars["Service Detection (-sV)"].set(True)
            self.scan_vars["OS Detection (-O)"].set(True)
            self.scan_vars["Intense Scan (Prompt)"].set(True)

    def run_network_scan(self):
        self.textbox_results.delete("1.0", "end")
        self.progress_bar.set(0)
        self.tabs.set("Results")

        subnet = self.entry_subnet.get().strip()
        if not subnet:
            messagebox.showerror("Error", "Please enter a subnet.")
            return

        nmap_command = ["nmap", "-sn", subnet]
        self.textbox_results.insert("end", f"Running: {' '.join(nmap_command)}\n\n")

        def run():
            process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.advanced_scan_results_raw = ""
            for line in process.stdout:
                self.advanced_scan_results_raw += line
                self.textbox_results.insert("end", line)
                self.textbox_results.see("end")
            self.progress_bar.set(1)

        threading.Thread(target=run).start()

    def run_advanced_scan(self):
        self.textbox_results.delete("1.0", "end")
        self.progress_bar.set(0)
        self.tabs.set("Results")

        target = self.entry_advanced_target.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target IP or hostname.")
            return

        selected_flags = []
        selected_keys = []
        intense_level = None

        for label, var in self.scan_vars.items():
            if var.get():
                selected_keys.append(label)
                if label == "Intense Scan (Prompt)":
                    try:
                        level = ctk.CTkInputDialog(text="Enter intensity level (1-5)", title="Intense Scan Level").get_input()
                        if level is None:
                            return
                        level = int(level)
                        if level < 1 or level > 5:
                            raise ValueError
                        intense_level = f"-T{level}"
                    except:
                        messagebox.showerror("Error", "Please enter a valid intensity level between 1 and 5.")
                        return
                else:
                    selected_flags.extend(self.scan_flags[label])

        if intense_level:
            selected_flags.append(intense_level)

        if not selected_flags:
            selected_flags = ["-T4", "-F"]

        if "Ping Scan (-sn)" in selected_keys and len(selected_keys) > 1:
            messagebox.showerror("Conflict", "Ping Scan (-sn) cannot be used with other options.")
            return

        if "Quick Scan (-T4 -F)" in selected_keys and "Port Scan (1-1000)" in selected_keys:
            messagebox.showerror("Conflict", "Quick Scan and Port Scan cannot be used together.")
            return

        nmap_command = ["nmap", "-vvv"] + selected_flags + [target]
        self.textbox_results.insert("end", f"Running: {' '.join(nmap_command)}\n\n")

        def run():
            process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.advanced_scan_results_raw = ""
            for line in process.stdout:
                self.advanced_scan_results_raw += line
                self.textbox_results.insert("end", line)
                self.textbox_results.see("end")
            self.progress_bar.set(1)

        threading.Thread(target=run).start()

    def export_to_pdf(self):
        if not self.advanced_scan_results_raw.strip():
            messagebox.showwarning("No Data", "No scan data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            try:
                logo_path = os.path.join(os.path.dirname(__file__), "logoblack.png")
                img = Image.open(logo_path).convert("RGBA")
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                logo = ImageReader(bg)
                c.drawImage(logo, (width - 140) / 2, height - 80, width=140, height=50)
            except Exception as e:
                print(f"Logo issue: {e}")

            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width / 2, height - 100, "Report")

            c.setFont("Courier", 10)
            text = c.beginText(40, height - 130)
            for line in self.advanced_scan_results_raw.splitlines():
                if text.getY() <= 50:
                    c.drawText(text)
                    c.showPage()
                    text = c.beginText(40, height - 50)
                    text.setFont("Courier", 10)
                text.textLine(line)
            c.drawText(text)

            c.setFont("Helvetica-Oblique", 10)
            footer = f"Report generated on JaalBreak | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            c.drawCentredString(width / 2, 30, footer)

            c.save()
            messagebox.showinfo("Exported", f"PDF saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")

if __name__ == "__main__":
    app = JaalBreak()
    app.mainloop()
