# Importa as dependências do Model e View
# Nota: O '.' é para importação relativa dentro do pacote 'app'.
from ..model.game_map import GameMap
from ..model.player import Player
from ..view.game_view import GameView 

class GameController:
    """
    Controlador principal do jogo.
    Gerencia o loop do jogo, processa comandos e coordena Model e View.
    """
    def __init__(self):
        # 1. Inicializa o Model (Mapa e Jogador)
        self.game_map = GameMap()
        
        # Pega a sala inicial e o limite de itens do mapa para inicializar o jogador
        start_room = self.game_map.get_start_room()
        max_itens = self.game_map.max_itens
        
        # O objeto Player é inicializado com a primeira sala (objeto Room)
        self.player = Player(current_room=start_room, max_itens=max_itens)
        
        # Inicializa a View
        self.view = GameView()
        
        # Estado do jogo
        self.running = True
        
        # Buffer de mensagem de feedback: Usado para exibir mensagens de erro/sucesso antes do redesenho da tela.
        self.feedback_message = ""
        
        # Controla a primeira execução
        self.first_execution = True

    def start_game(self):
        """Método principal para iniciar e rodar o loop do jogo."""
        
        # 1. Mensagens Iniciais (fora do loop para que o usuário possa ler)
        self.view.clear_terminal()
        self.view.display_message("--- Aventura RPG Iniciada! ---")
        self.view.display_message(f"Você pode carregar no máximo {self.player.max_itens} itens.")
        self.view.get_command("Pressione ENTER para começar...") # Pausa inicial

        while self.running:
            
            # CORREÇÃO: Limpa a tela em todas as iterações, EXCETO na primeira,
            # para que as mensagens iniciais sejam preservadas até o primeiro ENTER.
            if not self.first_execution:
                self.view.clear_terminal()
            
            # Define o first_execution como False imediatamente após a verificação
            # Isso garante que a tela será limpa no próximo ciclo.
            self.first_execution = False 

            # 2. Apresenta feedback do último comando, se houver
            if self.feedback_message:
                self.view.display_message(self.feedback_message)
                self.feedback_message = "" # Limpa o buffer
                
            # 3. Apresenta a sala atual e o inventário
            self.view.display_room(self.player.current_room)
            self.view.display_inventory(self.player.itens)

            # 4. Verifica condição de vitória (ou derrota/exit)
            if self.player.current_room.name == self.game_map.get_exit_room_name():
                self.view.display_message("\n*** PARABÉNS! Você encontrou a saída e completou a aventura! ***")
                self.view.get_command("Pressione ENTER para finalizar o jogo...")
                self.running = False
                break
                
            # 5. Pega o comando do usuário
            command_line = self.view.get_command()
            
            # 6. Processa o comando
            self.handle_command(command_line)

    def handle_command(self, command_line):
        """Processa a entrada do usuário e atualiza o estado do jogo."""
        
        # Normaliza o comando
        parts = command_line.lower().split()
        if not parts:
            return

        action = parts[0]
        target = parts[1] if len(parts) > 1 else None

        # Resetar o feedback antes de processar o novo comando
        self.feedback_message = ""

        if action in ['norte', 'sul', 'leste', 'oeste']:
            self._handle_move(action)
        elif action == 'pegar' and target:
            self._handle_take(target)
        elif action == 'largar' and target:
            self._handle_drop(target)
        elif action == 'usar' and target:
            self._handle_usar(target)
        elif action == 'sair':
            self.feedback_message = "Encerrando o jogo. Até a próxima!"
            self.running = False
        elif action == 'ajuda':
            self._display_help()
        else:
            # Comando inválido: Armazena a mensagem de erro no buffer para exibição no próximo ciclo
            self.feedback_message = "Comando inválido. Tente 'norte', 'pegar [item]', 'largar [item]', 'ajuda' ou 'sair'."


    def _handle_move(self, direction):
        """Lógica para movimentação entre salas."""
        direction_map = {
            'norte': 'north', 
            'sul': 'south', 
            'leste': 'east', 
            'oeste': 'west'
        }
        json_direction = direction_map.get(direction)
        
        current_room = self.player.current_room
        
        if json_direction in current_room.exits:
            next_room_name = current_room.exits[json_direction]
            next_room_object = self.game_map.get_room(next_room_name)
            
            if next_room_object:
                self.player.move(next_room_object) 
                # Note: Mudamos a exibição da mensagem para usar o buffer de feedback
                self.feedback_message = f"Você se moveu para o {direction.upper()}."
            else:
                self.feedback_message = "Erro no mapa: Sala de destino não encontrada."
        else:
            self.feedback_message = "Você não pode ir nessa direção."

    def _handle_take(self, item_name):
        """Lógica para pegar um item."""
        current_room = self.player.current_room
        
        item_description = current_room.get_item(item_name) 
        
        if item_description:
            if self.player.take_item(item_name, item_description):
                self.feedback_message = f"Você pegou '{item_name}'."
            else:
                current_room.add_item(item_name, item_description)
                self.feedback_message = "Seu inventário está cheio! Você precisa largar algo antes."
        else:
            self.feedback_message = f"Não há '{item_name}' nesta sala."
            
    def _handle_drop(self, item_name):
        """Lógica para largar um item."""
        
        item_description = self.player.drop_item(item_name) 
        
        if item_description:
            self.player.current_room.add_item(item_name, item_description)
            self.feedback_message = f"Você largou '{item_name}' na sala."
        else:
            self.feedback_message = f"Você não tem '{item_name}' no seu inventário."

    def _display_help(self):
        """Exibe os comandos disponíveis e pausa a tela."""
        # Não usamos o clear_terminal aqui para permitir que o feedback_message seja exibido.
        
        help_text = (
            "Comandos disponíveis:\n"
            "  norte, sul, leste, oeste  - Move o jogador.\n"
            "  pegar [item]             - Pega um item da sala. (Use o nome exato do item)\n"
            "  largar [item]            - Larga um item do inventário.\n"
            "  ajuda                    - Exibe este menu.\n"
            "  sair                     - Encerra o jogo."
        )
        self.view.display_message(help_text)
        # Pausa para o usuário ler a ajuda antes de retornar ao jogo, limpando a tela no próximo ciclo.
        self.view.get_command("\nPressione ENTER para voltar ao jogo...")

    def _handle_usar(self, item):
        """Lógica para usar item em uma sala."""
        if item in self.player.itens:
            item = self.player.current_room.get_useItem(item)
            self.feedback_message = f"Você está usando o item {item}\n {item[]}"
        else:
            self.feedback_message = f"Você não tem '{item}' no seu inventário."


