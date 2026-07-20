# ⚛️ Quantum Morse Code Encoder & Decoder

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-61DAFB?style=for-the-badge&logo=qiskit&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An interactive, full-stack quantum computing application built with **Qiskit** and **Streamlit**. This project demonstrates how classical information can be mapped into quantum states, transmitted over a simulated noisy physical channel, and decoded back into classical text using quantum circuit manipulation and measurement.

---

## 🌟 Overview

While sending Morse code over a quantum computer is a pedagogical exercise, this project serves as a functional prototype for the foundational concepts of **Quantum Communication** and **Quantum Key Distribution (QKD)**. 

The application takes standard classical text, translates it into Morse code, maps the dots and dashes into quantum states ($\vert{}0\rangle$ and $\vert{}1\rangle$), builds dynamic quantum circuits for each character, simulates physical hardware interference (Bit-Flip noise), and decodes the resulting measurements back into readable text while generating real-time radio telegraph audio.

---

## ✨ Key Features

*   **Dynamic Quantum Encoding:** Automatically generates custom Qiskit quantum circuits based on character length, mapping Morse symbols to ground and excited qubit states.
*   **Little-Endian Architecture Handling:** Implements automatic bit-string reversal to handle Qiskit's native right-to-left qubit indexing.
*   **Physical Noise Simulation:** Features an adjustable **Bit-Flip Error Model** (via `qiskit-aer`) that simulates environmental decoherence and hardware gate errors, allowing users to observe quantum entropy and signal corruption in real-time.
*   **Audio Synthesis Engine:** Uses NumPy and Python's native `wave` module to synthesize 700 Hz radio telegraph audio on the fly, letting users *hear* the exact difference between the clean transmitted signal and the noise-corrupted received signal.
*   **Interactive Web Interface:** Built with Streamlit, providing real-time circuit diagram rendering (via Matplotlib) and measurement histograms for 500-shot simulations.
*   **Automated Unit Testing:** Includes a standalone validation script (`teste_terminal.py`) to verify circuit logic and endianness prior to deployment.

---

## 🧠 Applied Quantum Concepts

This project is built around several core principles of quantum mechanics and quantum computation:

### 1. Quantum State Preparation
In classical computing, information is stored in bits (`0` or `1`). In our quantum communication channel, every qubit initializes by default in the ground state $\vert{}0\rangle$. Our protocol defines a standardized mapping:
*   **Morse Dot (`.`):** Mapped to the ground state $\vert{}0\rangle$ (no gate is applied).
*   **Morse Dash (`-`):** Mapped to the excited state $\vert{}1\rangle$.

### 2. The Pauli-X Gate (Quantum NOT)
To encode a dash (`-`), we must transition the qubit from $\vert{}0\rangle$ to $\vert{}1\rangle$. We achieve this by applying the **Pauli-X Gate** ($X$), which is the quantum analogue of the classical NOT gate. Mathematically, it corresponds to a $\pi$-radian rotation around the x-axis of the Bloch sphere, flipping the state vector:
$$X \vert{}0\rangle = \vert{}1\rangle$$

### 3. Measurement & Wavefunction Collapse
Once the quantum circuit is prepared, we apply measurement gates (`measure`) to all qubits. This action forces the quantum state to collapse into classical registers, yielding a deterministic bit string in an ideal, noise-free simulator.

### 4. Qiskit's Little-Endian Convention
A critical technical requirement when working with Qiskit is handling its **Little-Endian** bit numbering. Qiskit orders qubits from right to left (qubit 0 is the rightmost bit in the output string). For example, transmitting the Morse letter **"A"** (`.-` or $\vert{}0\rangle\vert{}1\rangle$) yields the raw Qiskit output string `10`. Our decoder implements an automatic string inversion (`[::-1]`) to recover the chronological order (`01`) before mapping it back to classical text.

### 5. Quantum Noise & Bit-Flip Errors
Real-world quantum hardware suffers from thermal fluctuation, electromagnetic interference, and gate imperfections. This project integrates `Qiskit Aer's NoiseModel` to inject **Bit-Flip Errors** (Pauli-$X$ errors) with a user-defined probability ($p$). When noise is introduced, a qubit intended to be $\vert{}0\rangle$ may spontaneously flip to $\vert{}1\rangle$ during transmission or readout, demonstrating the physical necessity of **Quantum Error Correction (QEC)** algorithms.

### 6. Connection to Quantum Key Distribution (QKD)
The state preparation technique used in this project is the exact mechanism that underlines cryptographic protocols like **BB84**. In QKD, sender and receiver encode cryptographic key bits into quantum states (such as photon polarizations). Because of the laws of quantum mechanics, any attempt by an eavesdropper to intercept the channel inevitably alters the quantum state, alerting the parties to the intrusion.

---

## 🛠️ Technology Stack

*   **Language:** Python 3.10+
*   **Quantum Framework:** Qiskit Core & Qiskit Aer
*   **Web Framework:** Streamlit
*   **Data Visualization:** Matplotlib & NumPy
*   **Circuit Rendering:** PyLaTeXenc

---

## 🚀 How to Run Locally

If you want to clone this repository and run the quantum simulation on your own local machine, follow the sequential steps below:

### 1. Clone the Repository
Open your terminal and clone the repository using Git:
```bash
git clone [https://github.com/YOUR-USERNAME/morse-quantico-streamlit.git](https://github.com/YOUR-USERNAME/morse-quantico-streamlit.git)
cd morse-quantico-streamlit
```

### 2. Create a Virtual Environment
We recommend using Conda (or standard Python venv) to isolate the quantum libraries:
```bash
conda create -n morse_quantico python=3.10 -y
conda activate morse_quantico
```

### 3. Install Dependencies
Install all required packages (Qiskit, Streamlit, PyLaTeXenc, etc.) via pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Backend Validation Suite
Before launching the web app, execute the automated CLI unit tests to verify the quantum logic and hardware endianness on your system:
```bash
python teste_terminal.py
```
*Expected output: `🚀 DIAGNÓSTICO FINAL: SISTEMA QUÂNTICO 100% VALIDADO!`*

### 5. Launch the Web Application
Start the Streamlit interactive server:
```bash
streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
morse-quantico-streamlit/
│
├── app.py                 # Main Streamlit web application & quantum engine
├── teste_terminal.py      # Automated CLI unit testing and validation script
├── requirements.txt       # Production dependencies for cloud deployment
└── README.md              # Project documentation
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute to this project—for example, by implementing **Superdense Coding** to transmit 2 classical bits per single physical qubit!

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).