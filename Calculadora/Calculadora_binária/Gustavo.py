# calculadora_binaria.py
"""
Calculadora binária para números de 1 byte com sinal.
Suporta operações de soma, subtração e multiplicação.
Valida entradas, detecta overflow e trabalha diretamente em binário.
"""

# Constantes para mensagens de erro
ERRO_TAMANHO = "tamanho da entrada invalido"
ERRO_VALOR = "valor invalido"
ERRO_OVERFLOW = "overflow"
OPERACOES_VALIDAS = {"+", "-", "x"}

def validar_entrada(bin_str: str) -> None:
    """Valida se a string contém apenas '0' ou '1' e tem 8 bits."""
    # Primeiro valida os valores (prioridade para o teste que espera "valor invalido")
    if not all(bit in "01" for bit in bin_str):
        raise Exception(ERRO_VALOR)
    # Depois valida o tamanho
    if len(bin_str) != 8:
        raise Exception(ERRO_TAMANHO)

def soma_binario(a: str, b: str) -> str:
    """Soma dois números binários de 8 bits, detectando overflow."""
    carry = 0
    resultado = ""
    for i in range(7, -1, -1):
        total = carry + int(a[i]) + int(b[i])
        carry = total // 2
        resultado = str(total % 2) + resultado
    # Overflow: se os sinais de a e b são iguais, mas o resultado tem sinal diferente
    if (a[0] == b[0]) and (resultado[0] != a[0]):
        raise Exception(ERRO_OVERFLOW)
    return resultado

def inverter_bits(bin_str: str) -> str:
    """Inverte os bits de uma string binária (complemento de um)."""
    return "".join("1" if bit == "0" else "0" for bit in bin_str)

def complemento_de_dois(bin_str: str) -> str:
    """Calcula o complemento de dois de um número binário."""
    inverted = inverter_bits(bin_str)
    return soma_binario(inverted, "00000001")

def subtrair_binario(a: str, b: str) -> str:
    """Subtrai dois números binários usando complemento de dois."""
    b_complemento = complemento_de_dois(b)
    return soma_binario(a, b_complemento)

def multiplicar_binario(a: str, b: str) -> str:
    """Multiplica dois números binários de 8 bits, detectando overflow."""
    # Determina o sinal do resultado
    sinal_resultado = "0" if a[0] == b[0] else "1"

    # Trabalha com valores absolutos (converte se negativo)
    a_val = complemento_de_dois(a) if a[0] == "1" else a
    b_val = complemento_de_dois(b) if b[0] == "1" else b

    resultado = "00000000"
    # Multiplicação bit a bit com deslocamento
    for i in range(7, -1, -1):
        if b_val[i] == "1":
            parcial = a_val + "0" * (7 - i)
            parcial = parcial[-8:]  # Garante 8 bits
            resultado = soma_binario(resultado, parcial)

    # Ajusta o sinal do resultado
    if sinal_resultado == "1":
        resultado = complemento_de_dois(resultado)

    # Verifica overflow
    if (resultado[0] == "0" and resultado > "01111111") or (resultado[0] == "1" and resultado < "10000000"):
        raise Exception(ERRO_OVERFLOW)

    return resultado

def calcular(n1: str, n2: str, operacao: str) -> str:
    """Função principal: realiza a operação binária solicitada."""
    # Valida entradas
    validar_entrada(n1)
    validar_entrada(n2)
    if operacao not in OPERACOES_VALIDAS:
        raise Exception(ERRO_VALOR)

    # Executa a operação correspondente
    if operacao == "+":
        return soma_binario(n1, n2)
    elif operacao == "-":
        return subtrair_binario(n1, n2)
    return multiplicar_binario(n1, n2)

def interface_interativa() -> None:
    """Interface interativa para o usuário."""
    print("=== Calculadora Binária (1 byte com sinal) ===")
    try:
        n1 = input("Digite o primeiro número binário (8 bits): ")
        n2 = input("Digite o segundo número binário (8 bits): ")
        operacao = input("Digite a operação (+, -, x): ")
        resultado = calcular(n1, n2, operacao)
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Erro: {str(e)}")

def testar() -> None:
    """Executa testes automáticos para validar o funcionamento."""
    casos = [
        ("00000001", "00000001", "+", "00000010"),
        ("00000010", "00000001", "-", "00000001"),
        ("11111111", "00000001", "+", "00000000"),
        ("11111111", "11111111", "+", "11111110"),
        ("00000010", "00000011", "x", "00000110"),
        ("11111111", "00000010", "x", "11111110"),
        ("11111111", "11111111", "x", "00000001"),
        ("01111111", "00000001", "+", "overflow"),
        ("10000000", "10000000", "+", "overflow"),
        ("0000001", "00000001", "+", "tamanho da entrada invalido"),
        ("00000001", "000000012", "+", "valor invalido"),
        ("00000001", "00000001", "/", "valor invalido"),
    ]
    print("\n=== Testes automáticos ===")
    for n1, n2, op, esperado in casos:
        try:
            resultado = calcular(n1, n2, op)
            status = "✅" if resultado == esperado else "❌"
            print(f"{status} {n1} {op} {n2} = {resultado}" + (f" (esperado: {esperado})" if resultado != esperado else ""))
        except Exception as e:
            status = "✅" if str(e) == esperado else "❌"
            print(f"{status} {n1} {op} {n2} lançou '{str(e)}'" + (f" (esperado: '{esperado}')" if str(e) != esperado else ""))

if __name__ == "__main__":
    interface_interativa()
    testar()  # Rodando os testes automaticamente