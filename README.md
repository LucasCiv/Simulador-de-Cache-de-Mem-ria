Simulador de Cache de Memória
Este projeto simula o funcionamento de uma cache de memória, incluindo o gerenciamento de linhas e conjuntos de cache. O objetivo é ilustrar como a memória cache funciona com relação à memória principal, utilizando técnicas de mapeamento e substituição.

Alunos
Lucas Thiago Dias Civardi
Funcionalidades
O simulador oferece as seguintes funcionalidades:

Cache associativa por conjunto: Com suporte a múltiplas linhas por conjunto.
Acesso à memória cache: Simulação do acesso à memória cache e busca de dados.
Manipulação de linhas e conjuntos: Gerenciamento de linhas e frequência de uso para possível substituição.
Classes Principais
LinhaCache: Representa uma linha de cache, armazenando a tag, os dados e a frequência de uso.
ConjuntoCache: Um conjunto de cache que contém múltiplas linhas de cache.
Cache: A cache principal que gerencia os conjuntos de cache e as operações de leitura e escrita de dados.
Métodos Importantes
acessar(endereco, tamanho_bloco, tag, indice, memoria_principal): Realiza o acesso à cache e verifica se a linha correspondente está presente no conjunto, com base no índice e na tag.
Como Executar
Certifique-se de que você tem o Python instalado.
Clone o repositório:
bash
Copiar código
git clone <url-do-repositorio>
Execute o script:
bash
Copiar código
python Script_Final.py
Contribuição
Faça um fork do projeto.
Crie um branch para a sua funcionalidade:
bash
Copiar código
git checkout -b minha-funcionalidade
Faça commit das suas mudanças:
bash
Copiar código
git commit -m 'Minha nova funcionalidade'
Envie as mudanças para o branch:
bash
Copiar código
git push origin minha-funcionalidade
Abra um Pull Request.
