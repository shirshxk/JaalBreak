# JaalBreak Scanner
![JaalBreak Logo](logo.png)
A simple network and port scanner built with Python and CustomTkinter.

---

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

### CLI

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

### GUI

```mermaid
flowchart TD
    A[Start GUI App] --> B[Show Sidebar & Tabs] --> C{User Chooses Tab}
    C -->|Scan| D[Enter Subnet]
    C -->|Advanced| E[Preset or Manual Flags]
    C -->|Help| F[Show Help Dialog]
    C -->|Exit| G[Close App]

    %% Scan Branch
    D --> H[Validate Input]
    H --> I[Build Nmap -sn]
    I --> J[Run Scan in Thread]
    J --> K[Stream Output to Textbox]
    K --> L{Export PDF?}
    L -->|Yes| M[Export with ReportLab]
    L -->|No| N[Skip Export]
    M --> O[Return to Tabs]
    N --> O
    O -.-> B

    %% Advanced Branch
    E --> P[Validate Flags/Conflicts]
    P --> Q[Build Advanced Command]
    Q --> J

    %% Help and Exit
    F --> R[Return to Tabs]
    G --> S[App Closed]
    R -.-> B

    %% Invisible links for horizontal balance
    D --- E
    E --- F
    F --- G

    %% STYLES - Strictly A-J cycling
    style A fill:#222,color:white
    style B fill:#333,color:white
    style C fill:#444,color:white
    style D fill:#555,color:white
    style E fill:#666,color:white
    style F fill:#777,color:white
    style G fill:#2d2d2d,color:white
    style H fill:#2a2a2a,color:white
    style I fill:#383838,color:white
    style J fill:#444,color:white
    style K fill:#555,color:white
    style L fill:#666,color:white
    style M fill:#777,color:white
    style N fill:#2d2d2d,color:white
    style O fill:#2a2a2a,color:white
    style P fill:#383838,color:white
    style Q fill:#444,color:white
    style R fill:#555,color:white
    style S fill:#666,color:white
```