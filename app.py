import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import wave
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

# Configuração visual da página Web no Streamlit
st.set_page_config(page_title="Morse Quântico com Áudio e Ruído", page_icon="⚛️", layout="wide")

# =====================================================================
# 1. DICIONÁRIOS E GERADOR DE ÁUDIO
# =====================================================================
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.'
}
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_DICT.items()}

def texto_para_morse(texto):
    """Converte o texto de entrada em uma lista de símbolos Morse."""
    texto_limpo = texto.upper().strip()
    morse_list = []
    caracteres_validos = []
    for char in texto_limpo:
        if char in MORSE_DICT:
            morse_list.append(MORSE_DICT[char])
            caracteres_validos.append(char)
    return morse_list, caracteres_validos

def gerar_audio_morse(morse_string, freq=700, wpm=15):
    """
    Sintetiza um arquivo de áudio WAV na memória com som de rádio telegrafo para o Morse.
    """
    dot_dur = 1.2 / wpm
    dash_dur = 3 * dot_dur
    pause_dur = dot_dur
    char_pause_dur = 3 * dot_dur
    sample_rate = 44100
    audio_data = []
    
    def gerador_senoide(duracao):
        t = np.linspace(0, duracao, int(sample_rate * duracao), False)
        seno = np.sin(freq * t * 2 * np.pi) * 32767
        # Suavização (fade in/out) para evitar sons de clique (pop noise) no alto-falante
        window = np.ones_like(seno)
        fade = min(200, len(seno) // 2)
        window[:fade] = np.linspace(0, 1, fade)
        window[-fade:] = np.linspace(1, 0, fade)
        return (seno * window).astype(np.int16)
    
    def gerador_silencio(duracao):
        return np.zeros(int(sample_rate * duracao), dtype=np.int16)
    
    for char in morse_string:
        if char == '.':
            audio_data.append(gerador_senoide(dot_dur))
            audio_data.append(gerador_silencio(pause_dur))
        elif char == '-':
            audio_data.append(gerador_senoide(dash_dur))
            audio_data.append(gerador_silencio(pause_dur))
        elif char == ' ':
            audio_data.append(gerador_silencio(char_pause_dur))
            
        if not audio_data:
            return None
            
    audio_final = np.concatenate(audio_data)
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_final.tobytes())
    wav_io.seek(0)
    return wav_io

# =====================================================================
# 2. CODIFICAÇÃO E RUÍDO QUÂNTICO
# =====================================================================
def criar_modelo_ruido(prob_erro):
    """Cria um modelo de ruído quântico de Bit-Flip na medição e portas."""
    noise_model = NoiseModel()
    if prob_erro > 0:
        # Erro que inverte |0> para |1> com probabilidade p
        erro_bit = pauli_error([('X', prob_erro), ('I', 1 - prob_erro)])
        noise_model.add_all_qubit_quantum_error(erro_bit, ['x'])
        noise_model.add_all_qubit_readout_error([[1 - prob_erro, prob_erro], [prob_erro, 1 - prob_erro]])
    return noise_model

def criar_circuito_morse(simbolo_morse):
    """Cria o circuito quântico (Ponto = |0>, Traço = |1> via Porta X)."""
    n_qubits = len(simbolo_morse)
    qc = QuantumCircuit(n_qubits, n_qubits)
    for index, simbolo in enumerate(simbolo_morse):
        if simbolo == '-':
            qc.x(index)
    qc.barrier()
    for i in range(n_qubits):
        qc.measure(i, i)
    return qc

def simular_e_decodificar(qc, noise_model):
    """Roda o circuito com o ruído físico e corrige o Little-Endian."""
    simulador = AerSimulator(noise_model=noise_model)
    job = simulador.run(qc, shots=500)
    resultado = job.result()
    contagens = resultado.get_counts()
    
    # O estado mais provável medido pelo receptor
    medicao_raw = max(contagens, key=contagens.get)
    medicao_corrigida = medicao_raw[::-1]
    
    morse_recuperado = ""
    for bit in medicao_corrigida:
        morse_recuperado += "." if bit == '0' else "-"
        
    letra_decodificada = REVERSE_MORSE_DICT.get(morse_recuperado, "?")
    return letra_decodificada, morse_recuperado, contagens

# =====================================================================
# INTERFACE GRÁFICA (STREAMLIT)
# =====================================================================
st.title("⚛️ Canal de Comunicação Quântica (Morse + Ruído)")
st.markdown(r"""
Este projeto implementa um canal de comunicação quântico completo:
1. **Codificação:** Mapeia **Pontos (`.`)** no estado **$|0\rangle$** e **Traços (`-`)** no estado **$|1\rangle$** usando a **Porta X**.
2. **Medição e Colapso:** Transfere a informação quântica para registradores clássicos.
3. **Decodificação:** Aplica o tratamento de **Little-Endian** do Qiskit para reverter a ordem dos bits e traduzir de volta para texto clássico.
""")

with st.sidebar:
    st.header("⚙️ Configurações do Canal")
    palavra_input = st.text_input("Palavra a transmitir:", value="SOS", max_chars=10)
    
    st.divider()
    st.subheader("🌪️ Interferência Física")
    taxa_ruido = st.slider("Taxa de Ruído Quântico (%)", min_value=0, max_value=50, value=0, step=5)
    prob_erro = taxa_ruido / 100.0
    
    st.divider()
    executar_btn = st.button("🚀 Transmitir Sinais", type="primary", use_container_width=True)

if executar_btn and palavra_input:
    morse_list, caracteres = texto_para_morse(palavra_input)
    
    if not caracteres:
        st.error("Digite apenas letras (A-Z) ou números (0-9).")
    else:
        morse_original_str = " ".join(morse_list)
        st.subheader(f"📡 Transmissão Original: **{'' .join(caracteres)}**")
        
        col1, col2 = st.columns([2, 2])
        with col1:
            st.info(f"**Código Morse Enviado:** `{morse_original_str}`")
        with col2:
            st.write("🔊 **Ouvir Sinal Original (Sem Ruído):**")
            audio_orig = gerar_audio_morse(morse_original_str)
            if audio_orig:
                st.audio(audio_orig, format="audio/wav")
                
        texto_final = ""
        morse_final_list = []
        modelo_ruido = criar_modelo_ruido(prob_erro)
        
        st.divider()
        st.write("### 🔬 Processamento Quântico sob Efeito de Interferência")
        
        for idx, (char, morse) in enumerate(zip(caracteres, morse_list)):
            st.markdown(f"#### Caractere: **{char}** | Alvo: `{morse}`")
            qc = criar_circuito_morse(morse)
            letra_decod, morse_decod, contagens = simular_e_decodificar(qc, modelo_ruido)
            
            texto_final += letra_decod
            morse_final_list.append(morse_decod)
            
            c1, c2 = st.columns([3, 2])
            with c1:
                st.write("**Circuito Quântico:**")
                fig, ax = plt.subplots(figsize=(6, 1.5 + len(morse)*0.3))
                qc.draw(output='mpl', ax=ax)
                st.pyplot(fig)
                plt.close(fig)
            with c2:
                st.write(f"**Histograma de Medição (Ruído: {taxa_ruido}%):**")
                st.bar_chart(contagens)
                
                # Alerta visual se o ruído corrompeu a letra
                if letra_decod == char:
                    st.success(f"**Sucesso:** `{morse_decod}` $\\rightarrow$ Letra **{letra_decod}**")
                else:
                    st.error(f"**Falha por Interferência:** `{morse_decod}` $\\rightarrow$ Lido como **{letra_decod}** (Era {char})")
            st.divider()
            
        # Resumo final da recepção
        morse_recebido_str = " ".join(morse_final_list)
        st.header("🏁 Resultado da Recepção no Destino")
        
        col_res1, col_res2 = st.columns([2, 2])
        with col_res1:
            if texto_final == "".join(caracteres):
                st.success(f"### Texto Recebido: **`{texto_final}`** (Sinal Limpo!)")
            else:
                st.warning(f"### Texto Recebido: **`{texto_final}`** (Sinal Corrompido!)")
            st.write(f"**Morse Recebido:** `{morse_recebido_str}`")
            
        with col_res2:
            st.write("🔊 **Ouvir Sinal Recebido (Com Efeito do Ruído):**")
            audio_rec = gerar_audio_morse(morse_recebido_str)
            if audio_rec:
                st.audio(audio_rec, format="audio/wav")