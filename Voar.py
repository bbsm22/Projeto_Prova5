import sys
import time
from collections import defaultdict
comeco_ts = time.time()
set_ts = 0
INf = 9999999999.9
VEL_AV = 800
class NF:
    def __init__(self,valor,Pso):
        self.Valor = valor
        self.Peso = Pso

    def __repr__(self):  
        return " (Valor = %r,Peso = %r)" % (self.Valor, self.Peso)

class Grafo:
    def __init__(self,N,Dir):
        self.Arestas = defaultdict(list)
        self.Avioes = defaultdict(list)
        self.NodosID = defaultdict(list)
        self.NodosSigla = defaultdict(list)
        self.LinhasAereas = defaultdict(list)
        self.Grau_Saida = [0]*N
        self.Grau_Entrada = [0]*N
        self.Direcionado = Dir
    
    def AtualizarNodo(self,z):
        self.NodosID[int(z[0])] = z
        self.NodosSigla[z[4]] = z
    def AdicionarAresta(self,z,A,B):
        chave = z[0] + ' - ' + z[2]
        self.Arestas[chave] = z
        self.Grau_Saida[A] += 1
        self.Grau_Entrada[B] += 1
        if(not self.Direcionado):
            chave = z[2] + ' - ' + z[0]
            self.Arestas[chave] = z
            self.Grau_Saida[B] += 1
            self.Grau_Entrada[A] += 1
    def AdicionarLinha(self, z):
        self.LinhasAereas[z[0]] = z
        
    def AdicionarAviao(self, z):
        self.Avioes[z[0]] = z

def DIJKSTRA(MatrizAdj,Peso, w, s,G):
    antecessor = [-1]*len(Peso)
    Peso[s] = 0
    ordenado = True
    F = []
    F.append(NF(s,0))
    while ((len(F) > 0)):
        u = Retira(F)
        if(u.Valor == w):
            break   
        if(MatrizAdj[u.Valor] != None):
            for v in MatrizAdj[u.Valor]:
                ordenado = relaxar(antecessor,Peso,u.Valor ,v.Valor, v.Peso,F,ordenado)
                if(not ordenado):
                    T = len(F)-1
                    sobe(F,T, T)
                    ordenado = True
    if(Resposta(Peso,antecessor,w,s,G) == 5):
        print("Nao Existe Caminho entre esses dois Aeroportos")

def TransformarHora(x):
    x = x/VEL_AV
    T = int(x)
    x -= T
    if(T >= 24):
        print(int(T/24),end = 'D ')
    T = T%24
    print(T,end='Hrs ')
    x *= 60
    L = (x - int(x))*10
    if(L > 5):
        x = int(x)+1
    else:
        x = int(x)
    print(x,end ='Min\n')
    
    
def Resposta(Peso,antecessor,w,s,G):
    caminho = []
    Saida = []
    print(Peso[w],'KM',end = ' -- ')
    TransformarHora(Peso[w])
    while(w != s):
        caminho.append(w)
        w = antecessor[w]
        if(w == -1):
            print("---")
            return 5
    caminho.append(w)
    for i in range(len(caminho)-1,-1,-1):
        if(antecessor[caminho[i]] != -1):
            ant = G.NodosID[antecessor[caminho[i]]+1][4]
            prox =  G.NodosID[caminho[i]+1][4]
            chave = ant + ' - ' + prox
            linhas = G.Arestas[chave][8].split()
            Equip = G.Arestas[chave][9].split()
            print(chave,G.Arestas[chave][4],'KM',end = ' -- ')
            TransformarHora(float(G.Arestas[chave][4]))
            print("Linhas Aereas:")
            for tg in range(0,len(linhas)):
                print(G.LinhasAereas[linhas[tg]][1],end = ' | ')
            print('')
            print("Avioes:")
            for tg in range(0,len(Equip)):
                print(G.Avioes[Equip[tg]][2],end = ' | ')
            print('')
        print('')
        k = caminho[i]+1
        print(k)
        M = []
        for u in range(0,5):
            M.append(G.NodosID[k][u])
        print(','.join(M))
        print('')
        print('')
    return 2

def relaxar(antecessor,p,u, v, w,F,O): 
    if(p[v] > p[u] + w):
        antecessor[v] = u 
        p[v] = p[u] +w
        F.append(NF(v,p[v]))
        return False
    return O

def Retira(F):
    T = len(F)-1
    aux = F[0]
    F[0] = F[T]
    F[T] = aux
    u= F.pop()
    MinimodoH(F,0, len(F)-1)
    return u

def minPorUltimo(F):
    menor = INf+1
    indice = 0
    for i in range(0,len(F)):
        if(F[i].Peso < menor):
            menor = F[i].Peso
            indice = i
    aux = F[len(F) - 1]
    F[len(F) - 1] = F[indice]
    F[indice] = aux

def esquerda(i):
    return 2*i + 1

def direita(i):
    return 2*i +2

def pai(i):
    return (i -1)//2

def MinimodoH(A,i, T):
    esq = esquerda(i)
    dir = direita(i) 
    if esq <= T and A[esq].Peso < A[i].Peso:
        menor = esq
    else:
        menor = i
    if dir <= T and A[dir].Peso < A[menor].Peso:
        menor = dir
    if menor != i:
        aux = A[i]
        A[i] = A[menor]
        A[menor] = aux
        return MinimodoH(A, menor, T)
    return A

def sobe(A,i, T):
    pa = pai(i)
    if pa >= 0 and A[pa].Peso < A[i].Peso:
        menor = pa
    else:
        menor = i
    if (menor == i) and( pa >= 0):
        aux = A[i]
        A[i] = A[pa]
        A[pa] = aux
        return sobe(A, pa, T)
    
def main():
    T = 0
    G = 0
    orig = '\\N'
    dest = '\\N'
    MatrizAdj = []
    for linha in sys.stdin:    
        if(T == 0):
            z = linha.split()
            N = int(z[0])
            G = Grafo(N,True)
            Peso = [INf]*N
            MatrizAdj = [0]*N
            for i in range(0,N):
                MatrizAdj[i] = []
            E = int(z[1])
            F = int(z[2])
            L = int(z[3])
            OP = int(z[4])
            if(OP == 0):
                orig = int(z[5]) - 1
                dest = int(z[6]) - 1
            elif(OP == 1):
                orig = z[5]
                dest = z[6]
            T += 1
        elif(T < E):
            if(linha[len(linha)-1] == '\n'):
                z = linha[:-1].split(',')
            else:
                z = linha.split(',')
            G.AtualizarNodo(z)
            T += 1
        elif(T < F):
            if(linha[len(linha)-1] == '\n'):
                z = linha[:-1].split(',')
            else:
                z = linha.split(',')
            A = int(z[1])-1
            B = int(z[3])-1
            w = float(z[4])
            chave = z[0] + ',' + z[2]
            MatrizAdj[A].append(NF(B,w))
            G.AdicionarAresta(z,A,B)
            T+=1
        elif(T < L):
            if(linha[len(linha)-1] == '\n'):
                z = linha[:-1].split(',')
            else:
                z = linha.split(',')
            G.AdicionarLinha(z)
            T +=1
        else:
            if(linha[len(linha)-1] == '\n'):
                z = linha[:-1].split(',')
            else:
                z = linha.split(',')
            G.AdicionarAviao(z)
    global set_ts
    set_ts = time.time()
    if(OP == 0):
        if(G.NodosID.get(orig+1,False) == False):
            print("Erro - Aeroporto Inválido")
            print(orig+1)
            return
        elif(G.NodosID.get(dest+1,False) == False):
            print("Erro - Aeroporto Inválido")
            print(dest+1)
            return
        if(G.Grau_Entrada[dest] == 0):
            print("Nao Existe nenhum voo chegando neste aeroporto")
            print(",".join(G.NodosID[dest+1]))
            return
        elif(G.Grau_Saida[orig] == 0):
            print("Nao Existe nenhum voo saindo deste aeroporto")
            print(",".join(G.NodosID[orig+1]))
            return
        p1 = G.NodosID[orig+1][4]
        p2 = G.NodosID[dest+1][4]
        chave = p1 + ' - ' + p2
        if((G.Arestas.get(chave,False))== False):
            DIJKSTRA(MatrizAdj,Peso,dest,orig,G)
        else:
            linhas = G.Arestas[chave][8].split()
            Equip = G.Arestas[chave][9].split()
            Dist = float(G.Arestas[chave][4])
            print(Dist,'KM',end = ' -- ')
            TransformarHora(Dist)
            M = []
            for u in range(0,5):
                M.append(G.NodosID[orig+1][u])
            print(','.join(M),end = "\n\n")
            print(chave,G.Arestas[chave][4])
            print("Linhas Aereas:")
            for tg in range(0,len(linhas)):
                print(G.LinhasAereas[linhas[tg]][1],end = ' | ')
            print('')
            print("Avioes:")
            for tg in range(0,len(Equip)):
                print(G.Avioes[Equip[tg]][2],end = ' | ')
            print('\n')
            M = []
            for u in range(0,5):
                M.append(G.NodosID[dest+1][u])
            print(','.join(M),end = "\n\n")
    elif(OP == 1):
        if(G.NodosSigla.get(orig,False) == False):
            print("Erro - Aeroporto Inválido")
            print(orig)
            return
        elif(G.NodosSigla.get(dest,False) == False):
            print("Erro - Aeroporto Inválido")
            print(dest)
            return
        chave = orig + ' - ' + dest
        if((G.Arestas.get(chave,False))== False):
            des= int(G.NodosSigla[dest][0]) - 1
            ori = int(G.NodosSigla[orig][0]) - 1
            if(G.Grau_Entrada[des] == 0):
                print("Nao Existe nenhum voo chegando neste aeroporto")
                print(",".join(G.NodosID[des+1]))
                return
            elif(G.Grau_Saida[ori] == 0):
                print("Nao Existe nenhum voo saindo deste aeroporto")
                print(",".join(G.NodosID[ori+1]))
                return
            DIJKSTRA(MatrizAdj,Peso,des,ori,G)
        else:
            linhas = G.Arestas[chave][8].split()
            Equip = G.Arestas[chave][9].split()
            Dist = float(G.Arestas[chave][4])
            print(Dist,'KM',end = ' -- ')
            TransformarHora(Dist)
            M = []
            for u in range(0,5):
                M.append(G.NodosSigla[orig][u])
            print(','.join(M),end = "\n\n")
            print(chave,G.Arestas[chave][4])
            print("Linhas Aereas:")
            for tg in range(0,len(linhas)):
                print(G.LinhasAereas[linhas[tg]][1],end = ' | ')
            print('')
            print("Avioes:")
            for tg in range(0,len(Equip)):
                print(G.Avioes[Equip[tg]][2],end = ' | ')
            print('\n')
            M = []
            for u in range(0,5):
                M.append(G.NodosSigla[dest][u])
            print(','.join(M),end = "\n\n")
    #print(orig,dest)
if __name__ == '__main__':
    main()
fim_ts = time.time()
razao = (set_ts - comeco_ts)/(fim_ts - comeco_ts)
#print((set_ts - comeco_ts)*(10**6))
#print((fim_ts - comeco_ts)*(10**6))
print(razao)


