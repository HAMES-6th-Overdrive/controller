# Controller ECU

<div align="center">

# 🎮 Vehicle Controller ECU

블루투스 기반 차량 제어 입력 및 데이터 전송 시스템

</div>

---

# 📌 Overview

본 프로젝트는 차량 제어를 위한
Controller ECU(Electronic Control Unit)를 구현한 프로젝트입니다.

사용자의 컨트롤러 입력 데이터를 수집하고,
Bluetooth 통신을 통해 HPC(High Performance Computer)로 전달합니다.

HPC에서는 수신한 제어 데이터를 처리한 뒤,
Ethernet 통신을 통해 ZCU(Zonal Control Unit)로 전송합니다.

실시간 입력 처리 및 안정적인 데이터 전송을 목표로 하며,
SDV(Software Defined Vehicle) 및
Zonal Architecture 기반 차량 구조를 고려하여 설계되었습니다.

---

# 🎯 Main Features

* 🎮 사용자 컨트롤러 입력 수집
* 📶 Bluetooth 기반 입력 데이터 전송
* 🌐 Ethernet 기반 HPC-ZCU 통신
* ⚡ 저지연 입력 처리
* 🚗 실시간 차량 제어 데이터 전달
* 🔄 Zonal Architecture 기반 통신 구조
* 🐧 Linux 기반 ECU 시스템

---

# 🏗️ System Architecture

```plaintext
┌─────────────────┐
│ User Controller │
│  Input Device   │
└────────┬────────┘
         │
         │ Bluetooth
         ▼
┌─────────────────┐
│       HPC       │
│ Input Processing│
│ Control Routing │
└────────┬────────┘
         │
         │ Ethernet
         ▼
┌─────────────────┐
│       ZCU       │
│ Control Receiver│
└─────────────────┘
```

---

# ⚙️ Tech Stack

## Hardware

* Raspberry Pi
* Game Controller / Input Device
* Vehicle Platform

## Software

* Python
* Linux (Ubuntu)
* Socket Programming

## Communication

* Bluetooth
* Ethernet TCP/IP

---

# 📂 Project Structure

```bash
controller/
├── bluetooth/        # Bluetooth communication
├── input/            # Controller input processing
├── communication/    # Ethernet communication
├── utils/            # Utility functions
├── docs/             # Documents
└── README.md
```

---

# 🚀 How It Works

1. 사용자 컨트롤러 입력 수집
2. Bluetooth 기반으로 HPC에 데이터 전달
3. HPC에서 입력 데이터 처리 수행
4. Ethernet 기반으로 ZCU에 데이터 전송
5. ZCU에서 제어 데이터 수신

---

# 🎮 Control Pipeline

```plaintext
User Controller
        ↓
Bluetooth Communication
        ↓
HPC Input Processing
        ↓
Ethernet Transmission
        ↓
ZCU
```

---

# 🖥️ Installation

## Clone Repository

```bash
git clone https://github.com/HAMES-6th-Overdrive/controller.git
cd controller
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

## Start Controller ECU

```bash
python main.py
```

---

# 📸 Demo

* Real-time controller input
* Bluetooth communication
* Ethernet data transmission
* Vehicle control data routing

---

# 📈 Expected Results

* 안정적인 컨트롤러 입력 처리
* 저지연 Bluetooth 통신
* 안정적인 Ethernet 데이터 전송
* 차량 시스템 연동 지원

---

# 🔥 Future Work

* 다양한 무선 컨트롤러 지원
* 입력 매핑 기능 추가
* OTA 기반 업데이트 시스템
* SDV 플랫폼 확장
* 통신 안정성 향상

---

# 👨‍💻 Team

HAMES 6th Overdrive Team

---

# 📄 License

This project is for educational and research purposes.
