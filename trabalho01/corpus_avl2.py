import re
import time
import unicodedata

#ETAPA 1 - etapa do pre-processamento
def preprocess_text(text):
    text = text.lower()             #aqui converto o texto em letras minusculas
    #text = re.sub(r'[^a-z ]', '', text)  # Remover caracteres não alfabéticos
    words = text.split()                 # Aqui eu faco a separacao do texto em palavras
    stopwords = set(["e", "ou", "mas", "a", "o", "os", "as", "são", "é"])  # Lista de palavras de parada
    words = [word for word in words if word not in stopwords]
    return words

# Exemplo de uso
text = "Programar em Python, Java e C++ é divertido."
print(text)
preprocessed_words = preprocess_text(text)
print(preprocessed_words)

#ETAPA 2 - construcao da arvore AVL

class Node:
    def __init__(self, value):    #aqui defino o valor e as referencias dos filhos da esquerda e direita na arvore
        self.value = value
        self.left_child = None
        self.right_child = None
        

class BST:
    def __init__(self):     #inicializo uma arvore BST vazia com este comando
        self.root = None
    
    def add(self, value):
    #aqui faco a insercao de um valor novo dentro da BST
        if self.root is None:
            self.root = Node(value)
        else:
            self._add_recursive(self.root, value)
    
    def _add_recursive(self, current_node, value):
    #aqui encontra a posicao correta de forma recursiva e insere um valor dentro da BST
        if value <= current_node.value:
            if current_node.left_child is None:
                current_node.left_child = Node(value)
            else:
                self._add_recursive(current_node.left_child, value)
        else:
            if current_node.right_child is None:
                current_node.right_child = Node(value)
            else:
                self._add_recursive(current_node.right_child, value)

    def _contains(self, current_node, value):
        #checando recursivamente se a BST contem o valor especificado, comecando pelo no dado
        if current_node is None:
            return False
        if current_node.value == value:
            return True
        if value < current_node.value:
            return self._contains(current_node.left_child, value)
        return self._contains(current_node.right_child, value)

    def contains(self, value):
        #checo se tem o valor especificado, caso tenha retornara True, c.c. sera False
        return self._contains(self.root, value)

class AVLNode(Node):
    #Herdo os atributos e metodos da classe Node
    def __init__(self, value):
    #Inicializo um no AVL com um valor dado
        super().__init__(value)
        self.height = 1
        self.bf = 0

    def calculate_height_and_bf(self):

        # Calculando a altura da subarvore do filho esquerdo
        left_height = 0
        if self.left_child is not None:
            left_height = self.left_child.height

        # Calculando a altura da subarvore do filho direito
        right_height = 0
        if self.right_child is not None:
            right_height = self.right_child.height

        # Atualizo a altura deste no
        self.height = 1 + max(left_height, right_height)

        # Calculo e atualizo o fator de balanceamento bf
        self.bf = left_height - right_height



class AVLTree(BST):
    #Herdo todos os atributos e metodos da BST e substitui alguns deles para manter a propriedade do equilibrio AVL
    def __init__(self):
        super().__init__()
    
    def add(self, value):
    #Vou substituir o metodo da adicao presente na classe BST para que ela lide com o balanceamento AVL
        self.root = self._add_recursive(self.root, value)

    def _add_recursive(self, current_node, value):
        if current_node is None:
           return AVLNode(value)

        if isinstance(current_node, Node) and not isinstance(current_node, AVLNode):
            current_node = AVLNode(current_node.value)
            current_node.left_child = self.root.left_child
            current_node.right_child = self.root.right_child
            self.root = current_node
    
        if value <= current_node.value:
            current_node.left_child = self._add_recursive(current_node.left_child, value)
        else:
            current_node.right_child = self._add_recursive(current_node.right_child, value)

        current_node.calculate_height_and_bf()

        if abs(current_node.bf) == 2:
            return self._balance(current_node)

        return current_node
    
    def get_height(self):
        if self.root is None:
            return 0
        return self.root.height
    
    def _rotate_left(self, node):   #Rotacionando pra esquerda

        
        pivot = node.right_child    # Guardo o pivo (a raiz da subarvore da direita do no)
        node.right_child = pivot.left_child     # Atualizo o filho da direita do no para o filho esquerdo do pivo
        pivot.left_child = node      # Aqui o filho esquerdo passara a ser o no


        node.calculate_height_and_bf()    # Recalculando a altura e o fator de balanceamento do no rotacionado
        pivot.calculate_height_and_bf()    # Recalculando a altura e o fator de balanceamento para o pivo

       
        return pivot     # Retornando o pivo como a nova raiz da subarvore

    def _rotate_right(self, node):  #Rotacionando para a direita

  
        pivot = node.left_child
        node.left_child = pivot.right_child
        pivot.right_child = node

        node.calculate_height_and_bf()
        pivot.calculate_height_and_bf()

        return pivot

    def _balance(self, node):
      # Case 1: (Subarvoress) L > R
      if node.bf == 2:
          pivot = node.left_child
          # Single right rotation (Right-right/direita-direita)
          if pivot.bf == 1:
              return self._rotate_right(node)
          # Double rotation: Left-Right/Esquerda-direita
          else:
              node.left_child = self._rotate_left(pivot)
              return self._rotate_right(node)
      # Case 2: (Subarvores) R > L
      else:
          pivot = node.right_child
          # Single left rotation (Left-left/esquerda-esquerda)
          if pivot.bf == -1:
              return self._rotate_left(node)
          # Double rotation: Right-Left/Direita-esquerda
          else:
              node.right_child = self._rotate_right(pivot)
              return self._rotate_left(node)

#ETAPA 3 - Autocompletar
    # ... outras funções p/ a etapa 3...

    def autocomplete(self, prefix):
        prefix = prefix.lower()
        results = []
        self._autocomplete_helper(self.root, prefix, results)
        return results

    def _autocomplete_helper(self, node, prefix, results):
        if node is None:
            return

        if node.value.startswith(prefix):
            results.append(node.value)

        if prefix < node.value:
            self._autocomplete_helper(node.left_child, prefix, results)
        else:
            self._autocomplete_helper(node.right_child, prefix, results)

# Código de comparação de desempenho

# Criar a árvore AVL e inserir palavras
avl_tree = AVLTree()
for word in preprocessed_words:
    avl_tree.add(word)

prefix = "p"
#vou usar o strip para remover as pontuações antes de incluir as palavras na lista
autocomplete_results = [word.strip(',.') for word in text.split() if word.lower().startswith(prefix)]


print("Palavras que começam com '{}':".format(prefix))
for word in autocomplete_results:
    normalized_word = unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8')
    normalized_prefix = unicodedata.normalize('NFKD', prefix).encode('ASCII', 'ignore').decode('utf-8')
    
    if normalized_word.startswith(normalized_prefix):
        highlighted_word = "\033[1;32m{}\033[m".format(word)  # Usar cor verde para destacar
        print(highlighted_word)
    else:
        print(word)

# Medir o tempo de busca na árvore AVL
start_time = time.time()
autocomplete_results = avl_tree.autocomplete("")
end_time = time.time()
search_time = end_time - start_time
print("Tempo de busca na AVL: {:.5f} segundos".format(search_time)) #:5f é a quantidade de nº a serem exibidos dps da virgula