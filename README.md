# JaalBreak Scanner
![JaalBreak Logo](logo.png)
JaalBreak is a Python-based network scanning tool featuring both a command-line interface (CLI) and a graphical user interface (GUI) using CustomTkinter. It is built on top of Nmap and designed for penetration testers, network analysts, and students.

## Features

- Dual Interface: CLI and GUI
- Preset-based scanning (Stealth, Aggressive, OS Detection, etc.)
- Subnet and individual IP scanning
- Real-time output from subprocess
- Threaded GUI execution to prevent freezing
- Export scan results as PDF using ReportLab
- Clean, styled GUI with CustomTkinter
- Input validation and conflict handling

## CLI Preview

```
$ python3 maincli.py

    _____                      __  _______                                 __       
   /     |                    /  |/       \                               /  |      
   $$$$$ |  ______    ______  $$ |$$$$$$$  |  ______    ______    ______  $$ |   __ 
      $$ | /      \  /      \ $$ |$$ |__$$ | /      \  /      \  /      \ $$ |  /  |
 __   $$ | $$$$$$  | $$$$$$  |$$ |$$    $$< /$$$$$$  |/$$$$$$  | $$$$$$  |$$ |_/$$/ 
/  |  $$ | /    $$ | /    $$ |$$ |$$$$$$$  |$$ |  $$/ $$    $$ | /    $$ |$$   $$<  
$$ \__$$ |/$$$$$$$ |/$$$$$$$ |$$ |$$ |__$$ |$$ |      $$$$$$$$/ /$$$$$$$ |$$$$$$  \ 
$$    $$/ $$    $$ |$$    $$ |$$ |$$    $$/ $$ |      $$       |$$    $$ |$$ | $$  |
 $$$$$$/   $$$$$$$/  $$$$$$$/ $$/ $$$$$$$/  $$/        $$$$$$$/  $$$$$$$/ $$/   $$/ 

Choose an option:
1. Scan
2. Help
3. Exit
```

## GUI Features

- Scan Tab: Basic subnet scan (Nmap -sn)
- Advanced Tab: Checkbox and dropdown flags
- Results Tab: Real-time output + PDF export
- Thread-safe subprocess handling
- Styled layout and input prompts

## Requirements

- Python 3.6+
- Nmap installed and available in PATH

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shirshxk/JaalBreak
    cd JaalBreak
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**

    ```bash
    python main.py
    ```

    **Note:** Make sure you have **nmap** installed and added to your system PATH for the scanner to function correctly.

---

## Runtime Architecture

```mermaid
flowchart TD
    A[Start CLI] --> B[Show Banner & Menu] --> C{User Chooses Option}
    C -->|Scan| D1[Prompt IP/Subnet]
    C -->|Advanced| D2[Prompt Flags/Presets]
    C -->|Help| D3[Show Help Info]
    C -->|Exit| D4[Exit Program]

    %% Scan Branch
    D1 --> E1{Scan Type?}
    E1 -->|Basic| F1[Build Nmap -sn]
    F1 --> G1[Execute Popen]
    G1 --> H1[Stream Output]
    H1 --> I1{Export PDF?}
    I1 -->|Yes| J1[Export with ReportLab]
    I1 -->|No| K1[Skip Export]
    J1 --> L1[Return to Menu]
    K1 --> L1
    L1 -.-> B

    %% Advanced Branch
    D2 --> E2[Validate]
    E2 --> F2[Build Advanced Command]
    F2 --> G1

    %% Help and Exit
    D3 --> M3[Return to Menu]
    D4 --> M4[Program Ends]
    M3 -.-> B

    %% Invisible links for horizontal balance
    D1 --- D2
    D2 --- D3
    D3 --- D4

    %% STYLES - cycled through all nodes
    style A fill:#222,color:white
    style B fill:#333,color:white
    style C fill:#444,color:white
    style D1 fill:#555,color:white
    style E1 fill:#666,color:white
    style F1 fill:#777,color:white
    style G1 fill:#2d2d2d,color:white
    style H1 fill:#2a2a2a,color:white
    style I1 fill:#383838,color:white
    style J1 fill:#444,color:white

    style D2 fill:#555,color:white
    style E2 fill:#666,color:white
    style F2 fill:#777,color:white

    style K1 fill:#2d2d2d,color:white
    style L1 fill:#2a2a2a,color:white

    style D3 fill:#383838,color:white
    style M3 fill:#444,color:white
    style D4 fill:#555,color:white
    style M4 fill:#666,color:white
```

## Running the Application

### CLI Version

```
python3 maincli.py
```

### GUI Version

```
python3 main.py
```

## File Structure

- `maincli.py`: CLI implementation
- `main.py`: GUI implementation using CustomTkinter
- `README.md`: This file

## Notes

- Works best on Linux or WSL with Nmap configured
- GUI is cross-platform but Nmap must be installed
- PDF export requires write permissions

## LICENSE

This project is licensed for educational and research purposes only, developed under the ST5062CEM Programming and Algorithm 2 module (Softwarica College).

---

## CREDITS

Developed by Shirshak Shrestha for coursework submission, July 2025

Course: Programming & Algorithm 2  
Module Code: ST5062CEM  
Instructor: Suman Shrestha
