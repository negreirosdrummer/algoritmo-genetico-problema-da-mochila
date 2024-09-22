import random

# Função para calcular o valor total e o peso total de um cromossomo
def fitness(cromossomo, itens, peso_maximo):
    peso_total = 0
    valor_total = 0
    for i in range(len(cromossomo)):
        if cromossomo[i] == 1:
            peso_total += itens[i][0]
            valor_total += itens[i][1]
    if peso_total > peso_maximo:
        return 0  # Se ultrapassar o peso máximo, fitness é zero
    return valor_total

# Função para gerar um cromossomo aleatório
def gerar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]

# Função para criar a população inicial
def criar_populacao(tamanho_populacao, tamanho_cromossomo):
    return [gerar_cromossomo(tamanho_cromossomo) for _ in range(tamanho_populacao)]

# Função para realizar o crossover entre dois cromossomos
def crossover(cromossomo1, cromossomo2):
    ponto_corte = random.randint(1, len(cromossomo1) - 1)
    filho1 = cromossomo1[:ponto_corte] + cromossomo2[ponto_corte:]
    filho2 = cromossomo2[:ponto_corte] + cromossomo1[ponto_corte:]
    return filho1, filho2

# Função para realizar a mutação em um cromossomo
def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  # Inverte o bit

# Função principal do algoritmo genético
def algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes, taxa_mutacao=0.01):
    # Criando a população inicial
    populacao = criar_populacao(numero_de_cromossomos, len(pesos_e_valores))
    melhor_por_geracao = []

    for geracao in range(geracoes):
        # Calculando o fitness de cada indivíduo
        fitness_populacao = [(fitness(individuo, pesos_e_valores, peso_maximo), individuo) for individuo in populacao]

        # Ordenando a população pelo valor fitness (maior para menor)
        fitness_populacao.sort(reverse=True, key=lambda x: x[0])
        melhor_individuo = fitness_populacao[0][1]
        melhor_valor = fitness_populacao[0][0]

        # Armazenando o melhor indivíduo da geração atual
        soma_valores = sum([pesos_e_valores[i][1] for i in range(len(melhor_individuo)) if melhor_individuo[i] == 1])
        melhor_por_geracao.append([soma_valores, melhor_individuo])

        # Seleção dos melhores indivíduos para reprodução (elitismo + roleta)
        nova_populacao = fitness_populacao[:numero_de_cromossomos // 2]  # Elitismo: mantém a metade superior
        nova_populacao = [individuo for _, individuo in nova_populacao]

        # Realizando o crossover para criar novos indivíduos
        while len(nova_populacao) < numero_de_cromossomos:
            pai1, pai2 = random.sample(nova_populacao[:numero_de_cromossomos // 2], 2)
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.extend([filho1, filho2])

        # Realizando a mutação nos novos indivíduos
        for individuo in nova_populacao:
            mutacao(individuo, taxa_mutacao)

        populacao = nova_populacao

    return melhor_por_geracao

# Exemplo de uso
pesos_e_valores = [ [2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400] ]
peso_maximo = 100
numero_de_cromossomos = 15
geracoes = 50

resultado = algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes)
for geracao, (soma_valores, cromossomo) in enumerate(resultado):
    print(f"Geração {geracao + 1}: Soma dos valores: {soma_valores:.2f}, Melhor cromossomo: {cromossomo}")
