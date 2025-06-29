import subprocess
import shutil
import ipaddress
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image

def ascii_banner():
    print(r"""

    _____                      __  _______                                 __       
   /     |                    /  |/       \                               /  |      
   $$$$$ |  ______    ______  $$ |$$$$$$$  |  ______    ______    ______  $$ |   __ 
      $$ | /      \  /      \ $$ |$$ |__$$ | /      \  /      \  /      \ $$ |  /  |
 __   $$ | $$$$$$  | $$$$$$  |$$ |$$    $$< /$$$$$$  |/$$$$$$  | $$$$$$  |$$ |_/$$/ 
/  |  $$ | /    $$ | /    $$ |$$ |$$$$$$$  |$$ |  $$/ $$    $$ | /    $$ |$$   $$<  
$$ \__$$ |/$$$$$$$ |/$$$$$$$ |$$ |$$ |__$$ |$$ |      $$$$$$$$/ /$$$$$$$ |$$$$$$  \ 
$$    $$/ $$    $$ |$$    $$ |$$ |$$    $$/ $$ |      $$       |$$    $$ |$$ | $$  |
 $$$$$$/   $$$$$$$/  $$$$$$$/ $$/ $$$$$$$/  $$/        $$$$$$$/  $$$$$$$/ $$/   $$/ 
                                                                                                      
    JAALBREAK SCANNER CLI
    """)

def print_menu():
    print("\nChoose an option:")
    print("1. Scan")
    print("2. Help")
    print("3. Exit")

def validate_nmap():
    if shutil.which("nmap") is None:
        print("[!] Nmap not found. Install it and add to PATH.")
        return False
    return True

def run_nmap_command(command):
    print(f"\n[+] Running: {' '.join(command)}\n")
    result = ""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line.strip())
            result += line
    except Exception as e:
        print(f"Error: {e}")
    return result

def prompt_export(result):
    while True:
        choice = input("\nDo you want to export the result to PDF? (y/n): ").strip().lower()
        if choice == 'y':
            filename = input("Enter PDF file name (without extension): ").strip()
            export_to_pdf(result, filename + ".pdf")
            break
        elif choice == 'n':
            break
        else:
            print("Invalid input. Enter 'y' or 'n'.")

def export_to_pdf(text, filepath):
    try:
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logoblack.png")
            img = Image.open(logo_path).convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            logo = ImageReader(bg)
            c.drawImage(logo, (width - 140) / 2, height - 80, width=140, height=50)
        except Exception as e:
            print(f"[!] Logo could not be added: {e}")

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 100, "JaalBreak Scan Report")

        c.setFont("Courier", 10)
        txt = c.beginText(40, height - 130)
        for line in text.splitlines():
            if txt.getY() <= 50:
                c.drawText(txt)
                c.showPage()
                txt = c.beginText(40, height - 50)
                txt.setFont("Courier", 10)
            txt.textLine(line)
        c.drawText(txt)

        footer = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 30, footer)

        c.save()
        print(f"[+] Report saved to {filepath}")
    except Exception as e:
        print(f"[!] Failed to export PDF: {e}")

def basic_scan():
    while True:
        subnet = input("Enter subnet (e.g. 192.168.1.0/24) or type 'back' to return: ").strip()
        if subnet.lower() == 'back':
            return
        try:
            ipaddress.ip_network(subnet)
            result = run_nmap_command(["nmap", "-sn", subnet])
            prompt_export(result)
            return
        except:
            print("[!] Invalid subnet format.")

def advanced_scan():
    while True:
        ip = input("Enter target IP address or subnet (type 'back' to return): ").strip()
        if ip.lower() == 'back':
            return
        try:
            ipaddress.ip_network(ip, strict=False)
            break
        except:
            print("[!] Invalid IP or subnet.")

    flags = {
        "Quick Scan (-T4 -F)": ["-T4", "-F"],
        "Ping Scan (-sn)": ["-sn"],
        "Port Scan (1-1000)": ["-p", "1-1000"],
        "UDP Scan (-sU)": ["-sU"],
        "Service Detection (-sV)": ["-sV"],
        "OS Detection (-O)": ["-O"],
        "Aggressive Scan (-A)": ["-A"]
    }

    while True:
        print("\nSelect scan options (comma separated, type 'back' to return):")
        for i, key in enumerate(flags, start=1):
            print(f"{i}. {key}")

        choices = input("Choice (e.g. 1,3,5): ").strip()
        if choices.lower() == 'back':
            return
        try:
            selected_flags = []
            selected_keys = [list(flags.keys())[int(i) - 1] for i in choices.split(',') if i.strip().isdigit()]
            if "Ping Scan (-sn)" in selected_keys and len(selected_keys) > 1:
                print("[!] Conflict: Ping Scan cannot be combined with others.")
                continue
            if "Quick Scan (-T4 -F)" in selected_keys and "Port Scan (1-1000)" in selected_keys:
                print("[!] Conflict: Quick Scan and Port Scan cannot be combined.")
                continue
            for key in selected_keys:
                selected_flags.extend(flags[key])
            if not selected_flags:
                selected_flags = ["-T4", "-F"]
            result = run_nmap_command(["nmap", "-vvv"] + selected_flags + [ip])
            prompt_export(result)
            return
        except Exception as e:
            print(f"[!] Error in input: {e}")

def show_help():
    print("""
    [ HELP ]
    - Basic Scan: Scans a subnet using ICMP ping.
    - Advanced Scan: Scans a single host with customizable options.
    - Make sure nmap is installed and in system PATH.
    """)

def main():
    while True:
        ascii_banner()
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            if not validate_nmap():
                continue
            while True:
                print("\nChoose scan type:")
                print("1. Basic Ping Scan")
                print("2. Advanced Scan")
                print("3. Back to Main Menu")
                scan_choice = input("Choice: ").strip()
                if scan_choice == '1':
                    basic_scan()
                elif scan_choice == '2':
                    advanced_scan()
                elif scan_choice == '3':
                    break
                else:
                    print("Invalid option. Try again.")

        elif choice == '2':
            show_help()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
