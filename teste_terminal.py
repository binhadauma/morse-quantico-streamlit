import sys
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

def imprimir_cabecalho(titulo):
    print("\n" + "=" * 60)
    print(f" 🧪 {titulo}")
    print("=" * 60)

# =====================================================================
# FUNÇÕES NÚCLEO (As mesmas usadas na aplicação principal)
# =====================================================================
def criar_circuito_morse(simbolo_morse):
    """Cria o circuito: '.' vira |0> e '-' vira |1> via porta X."""
    n_qubits = len(simbolo_morse)
    qc = QuantumCircuit(n_qubits, n_qubits)
    for index, simbolo in enumerate(simbolo_morse):
        if simbolo == '-':
            qc.x(index)
    for i in range(n_qubits):
        qc.measure(i, i)
    return qc

def simular(qc, noise_model=None, shots=1000):
    """Roda o circuito e retorna as contagens e a string corrigida."""
    simulador = AerSimulator(noise_model=noise_model)
    resultado = simulador.run(qc, shots=shots).result()
    contagens = resultado.get_counts()
    
    # Pega o resultado mais frequente e corrige o Little-Endian
    medicao_raw = max(contagens, key=contagens.get)
    medicao_corrigida = medicao_raw[::-1]
    
    morse_recuperado = ""
    for bit in medicao_corrigida:
        morse_recuperado += "." if bit == '0' else "-"
        
    return morse_recuperado, contagens, medicao_raw

# =====================================================================
# TESTE 1: VALIDAÇÃO DO CIRCUITO IDEAL E LITTLE-ENDIAN
# =====================================================================
imprimir_cabecalho("TESTE 1: Circuito Ideal e Inversão Little-Endian")

simbolo_teste = ".-."  # Letra 'R' em Morse
print(f"Símbolo Morse Alvo (Letra 'R'): {simbolo_teste}")
print("Expectativa de Qubits Preparados: |0⟩ |1⟩ |0⟩")

qc_ideal = criar_circuito_morse(simbolo_teste)
morse_res, contagens_ideal, raw_res = simular(qc_ideal)

print(f"\n[Qiskit Raw Output] Leitura bruta da direita para esquerda: '{raw_res}'")
print(f"[Correção Little-Endian] String invertida para leitura:     '{raw_res[::-1]}'")
print(f"[Tradução Morse] Símbolo recuperado após medição:          '{morse_res}'")
print(f"[Estatística] Contagem dos 1000 disparos (shots):           {contagens_ideal}")

if morse_res == simbolo_teste:
    print("\n✅ RESULTADO DO TESTE 1: APROVADO! Lógica quântica perfeita.")
else:
    print("\n❌ RESULTADO DO TESTE 1: FALHA! Erro na lógica de portas ou endianness.")
    sys.exit(1)

# =====================================================================
# TESTE 2: VALIDAÇÃO DO MODELO DE RUÍDO (BIT-FLIP)
# =====================================================================
imprimir_cabecalho("TESTE 2: Injeção de Ruído Quântico (30% Bit-Flip)")

prob_erro = 0.30
print(f"Simulando canal físico com {prob_erro * 100}% de interferência...")

# Criação do modelo de ruído
modelo_ruido = NoiseModel()
erro_bit = pauli_error([('X', prob_erro), ('I', 1 - prob_erro)])
modelo_ruido.add_all_qubit_quantum_error(erro_bit, ['x'])
modelo_ruido.add_all_qubit_readout_error([[1 - prob_erro, prob_erro], [prob_erro, 1 - prob_erro]])

_, contagens_ruido, _ = simular(qc_ideal, noise_model=modelo_ruido, shots=1000)

print("\n[Comparativo de Disparos (1000 shots)]")
print(f" -> Ambiente Ideal (Sem ruído): {contagens_ideal}")
print(f" -> Ambiente Ruidoso (30% erro): {contagens_ruido}")

# Verifica se o ruído realmente espalhou os resultados
if len(contagens_ruido) > 1:
    print("\n✅ RESULTADO DO TESTE 2: APROVADO! O modelo de ruído gerou entropia com sucesso.")
else:
    print("\n❌ RESULTADO DO TESTE 2: FALHA! O ruído não afetou os qubits.")

# =====================================================================
# TESTE 3: BATERIA AUTOMATIZADA DE APROVAÇÃO GERAL
# =====================================================================
imprimir_cabecalho("TESTE 3: Bateria de Aprovação em Lote")

dicionario_teste = {'A': '.-', 'B': '-...', 'Q': '--.-', 'S': '...', 'Z': '--..', '0': '-----'}
erros = 0

for letra, morse_alvo in dicionario_teste.items():
    qc = criar_circuito_morse(morse_alvo)
    morse_obtido, _, _ = simular(qc)
    
    status = "OK" if morse_obtido == morse_alvo else "ERRO"
    if status == "ERRO":
        erros += 1
    print(f" -> Letra [{letra}] | Alvo: {morse_alvo:<5} | Obtido: {morse_obtido:<5} | Status: [{status}]")

print("\n" + "-" * 60)
if erros == 0:
    print(" 🚀 DIAGNÓSTICO FINAL: SISTEMA QUÂNTICO 100% VALIDADO!")
    print(" O ambiente está pronto para executar a interface Streamlit.")
else:
    print(f" ⚠️ DIAGNÓSTICO FINAL: Foram encontrados {erros} erros na validação.")
print("-" * 60 + "\n")