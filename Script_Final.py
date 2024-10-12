#Obs o endereço na mémoria principal esta em decimal mas teve ser informado em binario para sua alocação correta na memoria cache.
#ALUNOS:
#LUCAS THIAGO DIAS CIVARDI
import os
import random
import math

class LinhaCache:
    def __init__(self):
        self.tag = None
        self.dado = None
        self.frequencia = 0

class ConjuntoCache:
    def __init__(self, num_linhas):
        self.linhas = [LinhaCache() for _ in range(num_linhas)]

class Cache:
    def __init__(self, num_conjuntos, linhas_por_conjunto):
        self.conjuntos = [ConjuntoCache(linhas_por_conjunto) for _ in range(num_conjuntos)]
        self.linhas_por_conjunto = linhas_por_conjunto

    def acessar(self, endereco, tamanho_bloco, tag, indice, memoria_principal):
        if indice < 0 or indice >= len(self.conjuntos):
            raise IndexError(f"Índice {indice} fora dos limites para cache com {len(self.conjuntos)} conjuntos.")
        
        conjunto_cache = self.conjuntos[indice]
        for i, linha in enumerate(conjunto_cache.linhas):
            if linha.tag == tag:
                linha.frequencia += 1
                return True, None, None, i
        
        linha_lfu = min(conjunto_cache.linhas, key=lambda x: x.frequencia)
        tag_substituida = linha_lfu.tag
        linha_substituida_index = conjunto_cache.linhas.index(linha_lfu)
        linha_lfu.tag = tag
        linha_lfu.dado = memoria_principal.ler(endereco)

        linha_lfu.frequencia = 1
        if tag_substituida is not None:
            return False, tag_substituida, linha_substituida_index, linha_substituida_index
        else:
            return False, None, None, linha_substituida_index

class MemoriaPrincipal:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.dados = [random.randint(0, 255) for _ in range(self.tamanho)]

    # Le o dado de um endereço especifico na memoria principal 
    def ler(self, endereco):
        if 0 <= endereco < self.tamanho:
            return self.dados[endereco]
        else:
            raise ValueError("Endereço fora dos limites da memória principal")
        
    # Escreve um valor em um endereço especifico na memoria principal
    def escrever(self, endereco, valor):
        if 0 <= endereco < self.tamanho:
            self.dados[endereco] = valor
        else:
            raise ValueError("Endereço fora dos limites da memória principal")
        
# Le o arquivo de configuração e retorna os parametros necessarios para inicializar a memoria e a cache
def ler_arquivo_configuracao(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            tamanho_mp_kb = int(arquivo.readline().strip()) * 1024  # Tamanho em bytes
            palavras_por_bloco = int(arquivo.readline().strip())
            tamanho_cache_kb = int(arquivo.readline().strip()) * 1024  # Tamanho em bytes
            linhas_por_conjunto = int(arquivo.readline().strip())
            
            tamanho_mp = tamanho_mp_kb // 4  # Converte de bytes para número de palavras
            tamanho_cache = tamanho_cache_kb
            
        return tamanho_mp, palavras_por_bloco, tamanho_cache, linhas_por_conjunto
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None
    except ValueError:
        print(f"Erro: O arquivo '{caminho_arquivo}' contém valores inválidos.")
        return None
    
# Le o arquivo de endereços e retorna uma lista com os endereços a serem acessados
def ler_arquivo_enderecos(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            enderecos = [linha.strip() for linha in arquivo.readlines()]
        return enderecos
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None
    
# Converte um endereço binario para um inteiro
def bin_to_int(endereco_binario):
    try:
        return int(endereco_binario, 2)
    except ValueError:
        raise ValueError(f"Endereço binário inválido: {endereco_binario}")

def exibir_estado_cache(cache, contador_acertos, contador_falhas, contador_substituicoes):
    for i, conjunto in enumerate(cache.conjuntos):
        print(f"Conjunto {i}:")
        for j, linha in enumerate(conjunto.linhas):
            print(f"  Linha {j}: Tag={linha.tag}, Dado={linha.dado}, Frequência={linha.frequencia}")
    print(f"Cache Hit: {contador_acertos}")
    print(f"Cache Miss: {contador_falhas}")
    print(f"Substituições: {contador_substituicoes}")

    taxa_acertos = contador_acertos / (contador_acertos + contador_falhas) if (contador_acertos + contador_falhas) > 0 else 0
    taxa_falhas = contador_falhas / (contador_acertos + contador_falhas) if (contador_acertos + contador_falhas) > 0 else 0
    print(f"Taxa de Acertos: {taxa_acertos:.2f}")
    print(f"Taxa de Falhas: {taxa_falhas:.2f}")

def exibir_detalhes_conjunto(cache, indice):
    def exibir_conjunto(conjunto, indice):
        print(f"Conjunto {indice}:")
        for i, linha in enumerate(conjunto.linhas):
            print(f"  Linha {i}: Tag={linha.tag}, Dado={linha.dado}, Frequência={linha.frequencia}")

    print(f"Detalhes do conjunto atual:")
    exibir_conjunto(cache.conjuntos[indice], indice)

    if indice > 0:
        print(f"Detalhes do conjunto antecessor:")
        exibir_conjunto(cache.conjuntos[indice - 1], indice - 1)
    else:
        print(f"Conjunto antecessor não disponível (índice fora do alcance).")

    if indice < len(cache.conjuntos) - 1:
        print(f"Detalhes do conjunto sucessor:")
        exibir_conjunto(cache.conjuntos[indice + 1], indice + 1)
    else:
        print(f"Conjunto sucessor não disponível (índice fora do alcance).")

def calcular_bits(tamanho_mp, palavras_por_bloco, tamanho_cache, linhas_por_conjunto):
    endereco_bits = int(math.log2(tamanho_mp))
    bloco_bits = int(math.log2(palavras_por_bloco))
    num_bloco_mp = endereco_bits - bloco_bits
    num_conjuntos = tamanho_cache // (linhas_por_conjunto * palavras_por_bloco * 4)
    conjunto_bits = int(math.log2(num_conjuntos))
    tag_bits = num_bloco_mp - conjunto_bits
    return endereco_bits, bloco_bits, conjunto_bits, tag_bits, num_bloco_mp

def main():
    cache = None
    memoria_principal = None
    contador_acertos = 0
    contador_falhas = 0
    contador_substituicoes = 0
    endereco_bits = bloco_bits = conjunto_bits = tag_bits = num_bloco_mp = None

    while True:
        print("\nMenu:")
        print("1. Carregar arquivo de configuração")
        print("2. Carregar arquivo de endereços")
        print("3. Acessar endereço")
        print("4. Exibir estado atual da cache")
        print("5. Exibir configuração dos bits")
        print("6. Exibir memória principal")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            caminho_configuracao = input("Informe o caminho do arquivo de configuração: ")
            config = ler_arquivo_configuracao(caminho_configuracao)
            if config:
                tamanho_mp, palavras_por_bloco, tamanho_cache, linhas_por_conjunto = config
                memoria_principal = MemoriaPrincipal(tamanho_mp)
                num_conjuntos = tamanho_cache // (linhas_por_conjunto * palavras_por_bloco * 4)
                cache = Cache(num_conjuntos, linhas_por_conjunto)
                endereco_bits, bloco_bits, conjunto_bits, tag_bits, num_bloco_mp = calcular_bits(
                    tamanho_mp, palavras_por_bloco, tamanho_cache, linhas_por_conjunto)
                print("Configuração carregada com sucesso.")

        elif opcao == '2':
            if not cache or not memoria_principal:
                print("Erro: Carregue a configuração primeiro.")
                continue

            caminho_enderecos = input("Informe o caminho do arquivo de endereços: ")
            enderecos = ler_arquivo_enderecos(caminho_enderecos)
            if enderecos:
                for endereco_binario in enderecos:
                    try:
                        endereco = bin_to_int(endereco_binario)
                        tag = endereco >> (bloco_bits + conjunto_bits)
                        indice = (endereco >> bloco_bits) & ((1 << conjunto_bits) - 1)
                        bloco_offset = endereco & ((1 << bloco_bits) - 1)
                        hit, tag_substituida, linha_substituida_index, linha_alocada_index = cache.acessar(
                            endereco, palavras_por_bloco, tag, indice, memoria_principal)
                        if hit:
                            contador_acertos += 1
                            print(f"Cache Hit! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}.")
                        else:
                            contador_falhas += 1
                            if tag_substituida is not None:
                                contador_substituicoes += 1
                                print(f"Cache Miss! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}. Linha {linha_substituida_index} substituída.")
                            else:
                                print(f"Cache Miss! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}.")
                        exibir_detalhes_conjunto(cache, indice)
                    except ValueError as ve:
                        print(f"Erro ao acessar endereço binário '{endereco_binario}': {ve}")

        elif opcao == '3':
            if not cache or not memoria_principal:
                print("Erro: Carregue a configuração primeiro.")
                continue

            endereco_binario = input("Informe o endereço binário: ")
            try:
                endereco = bin_to_int(endereco_binario)
                tag = endereco >> (bloco_bits + conjunto_bits)
                indice = (endereco >> bloco_bits) & ((1 << conjunto_bits) - 1)
                bloco_offset = endereco & ((1 << bloco_bits) - 1)
                hit, tag_substituida, linha_substituida_index, linha_alocada_index = cache.acessar(
                    endereco, palavras_por_bloco, tag, indice, memoria_principal)
                if hit:
                    contador_acertos += 1
                    print(f"Cache Hit! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}.")
                else:
                    contador_falhas += 1
                    if tag_substituida is not None:
                        contador_substituicoes += 1
                        print(f"Cache Miss! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}. Linha {linha_substituida_index} substituída.")
                    else:
                        print(f"Cache Miss! Endereço {endereco_binario} (decimal {endereco}) alocado na linha {linha_alocada_index} do conjunto {indice}.")
                exibir_detalhes_conjunto(cache, indice)
            except ValueError as ve:
                print(f"Erro ao acessar endereço binário '{endereco_binario}': {ve}")

        elif opcao == '4':
            if not cache:
                print("Erro: Carregue a configuração primeiro.")
                continue

            exibir_estado_cache(cache, contador_acertos, contador_falhas, contador_substituicoes)

        elif opcao == '5':
            if endereco_bits is not None:
                print(f"Bits endereço: {endereco_bits}")
                print(f"Bits S: {num_bloco_mp}")
                print(f"Bits W: {bloco_bits}")
                print(f"Bits D: {conjunto_bits}")
                print(f"Bits Tag: {tag_bits}")
                
            else:
                print("Configuração não carregada.")

        elif opcao == '6':
            if not memoria_principal:
                print("Erro: Carregue a configuração primeiro.")
                continue

            print("Memória Principal:")
            for i, dado in enumerate(memoria_principal.dados):
                print(f"Endereço {i}: Dado={dado}")
            else:
                print("Memória principal configurada.")
        
        elif opcao == '7':
            if cache:
                print("Cache na saída:")
                exibir_estado_cache(cache, contador_acertos, contador_falhas, contador_substituicoes)
                taxa_falhas = contador_falhas / (contador_acertos + contador_falhas) if (contador_acertos + contador_falhas) > 0 else 0
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()