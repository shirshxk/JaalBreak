import subprocess
import shutil
import ipaddress
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
from colorama import Fore, Style, init

init(autoreset=True)

def ascii_banner():
    print(Fore.CYAN + r"""

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
    print(Fore.YELLOW + "\nChoose an option:")
    print(Fore.CYAN + "1." + Fore.WHITE + " Scan")
    print(Fore.CYAN + "2." + Fore.WHITE + " Help")
    print(Fore.CYAN + "3." + Fore.WHITE + " Exit")

def validate_nmap():
    if shutil.which("nmap") is None:
        print(Fore.RED + "[!] Nmap not found. Install it and add to PATH.")
        return False
    return True

def run_nmap_command(command):
    print(Fore.GREEN + f"\n[+] Running: {' '.join(command)}\n")
    result = ""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(Fore.WHITE + line.strip())
            result += line
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
    return result

def prompt_export(result):
    while True:
        choice = input(Fore.YELLOW + "\nDo you want to export the result in PDF? (y/n): " + Fore.WHITE).strip().lower()
        if choice == 'y':
            filename = input(Fore.YELLOW + "Enter PDF file name (without extension): " + Fore.WHITE).strip()
            export_to_pdf(result, filename + ".pdf")
            break
        elif choice == 'n':
            break
        else:
            print(Fore.RED + "Invalid input. Enter 'y' or 'n'.")

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
            print(Fore.YELLOW + f"[!] Logo could not be added: {e}")

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
        print(Fore.GREEN + f"[+] Report saved to {filepath}")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to export PDF: {e}")

def prompt_intensity():
    while True:
        level = input(Fore.YELLOW + "Do you want to add intensity level (-T)? Enter 1–5 or press Enter to skip: " + Fore.WHITE).strip()
        if not level:
            return None
        if level in ['1','2','3','4','5']:
            return f"-T{level}"
        print(Fore.RED + "[!] Invalid intensity level.")

def basic_scan():
    while True:
        subnet = input(Fore.YELLOW + "Enter subnet (e.g. 192.168.1.0/24) or type 'back' to return: " + Fore.WHITE).strip()
        if subnet.lower() == 'back':
            return
        try:
            ipaddress.ip_network(subnet)
            result = run_nmap_command(["nmap", "-sn", subnet])
            prompt_export(result)
            return
        except:
            print(Fore.RED + "[!] Invalid subnet format.")

def advanced_scan():
    while True:
        ip = input(Fore.YELLOW + "Enter target IP address or subnet (type 'back' to return): " + Fore.WHITE).strip()
        if ip.lower() == 'back':
            return
        try:
            ipaddress.ip_network(ip, strict=False)
            break
        except:
            print(Fore.RED + "[!] Invalid IP or subnet.")

    presets = {
        "Default": ["-T4", "-F"],
        "Stealth": ["-sS", "-Pn"],
        "Aggressive": ["-A"],
        "Custom": []
    }

    print(Fore.YELLOW + "\nAvailable Presets:")
    for i, name in enumerate(presets.keys(), 1):
        print(Fore.CYAN + f"{i}." + Fore.WHITE + f" {name}")
    preset_choice = input(Fore.YELLOW + "Choose a preset (or press Enter to skip): " + Fore.WHITE).strip()

    selected_flags = []
    if preset_choice.isdigit() and 1 <= int(preset_choice) <= len(presets):
        selected_flags = presets[list(presets.keys())[int(preset_choice)-1]]

    if not selected_flags:
        flags = {
            "Quick Scan (-T4 -F)": ["-T4", "-F"],
            "Ping Scan (-sn)": ["-sn"],
            "Port Scan (1-1000)": ["-p", "1-1000"],
            "UDP Scan (-sU)": ["-sU"],
            "Service Detection (-sV)": ["-sV"],
            "OS Detection (-O)": ["-O"],
            "Aggressive Scan (-A)": ["-A"],
            "Custom Intensity (-Tn) Only": []
        }
        print(Fore.YELLOW + "\nSelect scan options (comma separated, type 'back' to return):")
        for i, key in enumerate(flags, start=1):
            print(Fore.CYAN + f"{i}." + Fore.WHITE + f" {key}")

        choices = input(Fore.YELLOW + "Choice (e.g. 1,3,5): " + Fore.WHITE).strip()
        if choices.lower() == 'back':
            return
        try:
            selected_keys = [list(flags.keys())[int(i) - 1] for i in choices.split(',') if i.strip().isdigit()]
            if "Ping Scan (-sn)" in selected_keys and len(selected_keys) > 1:
                print(Fore.RED + "[!] Conflict: Ping Scan cannot be combined with others.")
                return
            if "Quick Scan (-T4 -F)" in selected_keys and "Port Scan (1-1000)" in selected_keys:
                print(Fore.RED + "[!] Conflict: Quick Scan and Port Scan cannot be combined.")
                return
            for key in selected_keys:
                selected_flags.extend(flags[key])
        except Exception as e:
            print(Fore.RED + f"[!] Error in input: {e}")
            return

    intensity_flag = prompt_intensity()
    if intensity_flag:
        selected_flags = [f for f in selected_flags if not f.startswith("-T")]
        selected_flags.append(intensity_flag)

    result = run_nmap_command(["nmap", "-vvv"] + selected_flags + [ip])
    prompt_export(result)

def show_help():
    print(Fore.CYAN + """
    [ HELP ]
    - Basic Scan: Scans a subnet using ICMP ping.
    - Advanced Scan: Scans a single host with customizable options.
    - Presets simplify scan selection: Default, Stealth, Aggressive, or Custom.
    - Make sure nmap is installed and in system PATH.
    """)

def main():
    while True:
        ascii_banner()
        print_menu()
        choice = input(Fore.YELLOW + "Enter your choice: " + Fore.WHITE).strip()

        if choice == '1':
            if not validate_nmap():
                continue
            while True:
                print(Fore.YELLOW + "\nChoose scan type:")
                print(Fore.CYAN + "1." + Fore.WHITE + " Basic Ping Scan")
                print(Fore.CYAN + "2." + Fore.WHITE + " Advanced Scan")
                print(Fore.CYAN + "3." + Fore.WHITE + " Back to Main Menu")
                scan_choice = input(Fore.YELLOW + "Choice: " + Fore.WHITE).strip()
                if scan_choice == '1':
                    basic_scan()
                elif scan_choice == '2':
                    advanced_scan()
                elif scan_choice == '3':
                    break
                else:
                    print(Fore.RED + "Invalid option. Try again.")

        elif choice == '2':
            show_help()
        elif choice == '3':
            print(Fore.GREEN + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")

if __name__ == "__main__":
    main()
