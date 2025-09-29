from collections import defaultdict
import heapq

def dijkstra(grafo, inicio):
    dist = {v: float("inf") for v in grafo}
    dist[inicio] = 0
    anterior = {v: None for v in grafo}
    fila = [(0, inicio)]

    while fila:
        d, u = heapq.heappop(fila)
        if d > dist[u]:
            continue
        for v, peso in grafo[u]:
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                anterior[v] = u
                heapq.heappush(fila, (dist[v], v))
    return dist, anterior

def reconstruir_caminho(anterior, destino):
    caminho = []
    while destino is not None:
        caminho.append(destino)
        destino = anterior[destino]
    return caminho[::-1]

def gerar_emparelhamentos(nos):
    if not nos:
        yield []
        return
    u = nos[0]
    for i in range(1, len(nos)):
        v = nos[i]
        resto = nos[1:i] + nos[i+1:]
        for m in gerar_emparelhamentos(resto):
            yield [(u, v)] + m

def carteiro_chines(grafo):
    custo_original = sum(peso for u in grafo for _, peso in grafo[u]) // 2
    impares = [u for u in grafo if len(grafo[u]) % 2 == 1]

    if not impares:
        return custo_original, [], grafo

    distancias = {}
    caminhos = {}
    for u in impares:
        dist, ant = dijkstra(grafo, u)
        for v in impares:
            if u != v:
                distancias[(u, v)] = dist[v]
                caminhos[(u, v)] = reconstruir_caminho(ant, v)

    melhor_custo = float("inf")
    melhor = None
    for m in gerar_emparelhamentos(impares):
        c = sum(distancias[(u, v)] for u, v in m)
        if c < melhor_custo:
            melhor_custo = c
            melhor = m

    multigrafo = {u: [v for v, _ in grafo[u]] for u in grafo}
    for u, v in melhor:
        caminho = caminhos[(u, v)]
        for a, b in zip(caminho, caminho[1:]):
            multigrafo[a].append(b)
            multigrafo[b].append(a)

    custo_total = custo_original + melhor_custo
    return custo_total, melhor, multigrafo

def ciclo_euleriano(grafo, inicio):
    g = {u: list(vs) for u, vs in grafo.items()}
    pilha = [inicio]
    ciclo = []

    while pilha:
        u = pilha[-1]
        if g[u]:
            v = g[u].pop()
            g[v].remove(u)
            pilha.append(v)
        else:
            ciclo.append(pilha.pop())
    return ciclo[::-1]

if __name__ == "__main__":
    grafo = {
        'A': [('B',5), ('C',2), ('D',8)],
        'B': [('A',5), ('C',6), ('E',11)],
        'C': [('A',2), ('B',6), ('D',5), ('E',12)],
        'D': [('A',8), ('C',5), ('E',9)],
        'E': [('B',11), ('C',12), ('D',9)]
    }

    custo, pares, multigrafo = carteiro_chines(grafo)
    print("Custo mínimo para percorrer todas as ruas:", custo)
    print("Emparelhamentos de nós ímpares escolhidos:", pares)

    ciclo = ciclo_euleriano(multigrafo, 'A')
    print("ciclo Euleriano do carteiro:")
    print(" -> ".join(ciclo))
