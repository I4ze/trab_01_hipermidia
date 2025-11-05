from ..model.game_map import GameMap
from ..model.player import Player
from ..view.game_view import GameView 

class GameController:
    """
    Controlador principal do jogo.
    Gerencia o loop do jogo, processa comandos e coordena Model e View.
    """
    def __init__(self):
        self.game_map = GameMap()
        
        start_room = self.game_map.get_start_room()
        max_itens = self.game_map.max_itens
        self.player = Player(current_room=start_room, max_itens=max_itens)
        
        self.view = GameView()
        self.running = True
        self.feedback_message = ""

    def start_game(self):
        """Método principal para iniciar e rodar o loop do jogo."""
        self.view.clear_terminal()
        self.view.display_message("--- Aventura Iniciada! ---")
        self.view.display_message(f"Você pode carregar no máximo {self.player.max_itens} itens.")
        self.view.get_command("Pressione ENTER para começar...")

        while self.running:
            self.view.clear_terminal()

            if self.feedback_message:
                self.view.display_message(self.feedback_message)
                self.feedback_message = ""
                
            self.view.display_room(self.player.current_room)
            self.view.display_inventory(self.player.itens)

            if self.player.current_room.name == self.game_map.get_exit_room_name():
                self.view.display_message("\n*** Você encontrou a saída e completou a aventura! ***")
                self.view.get_command("Pressione ENTER para finalizar o jogo...")
                self.running = False
                break
                
            command_line = self.view.get_command()
            self.handle_command(command_line)

    def handle_command(self, command_line):
        """Processa a entrada do usuário e atualiza o estado do jogo."""
        parts = command_line.lower().split()
        if not parts:
            return

        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        self.feedback_message = ""

        if action in ['norte', 'sul', 'leste', 'oeste', 'cima', 'baixo']:
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
            self.feedback_message = "Comando inválido. Tente 'norte', 'pegar [item]', 'largar [item]', 'usar [item]', 'ajuda' ou 'sair'."

    def _handle_move(self, direction):
        """Lógica para movimentação entre salas (incluindo trancas e up/down)."""
        if self.player.current_room.monster:
            self.feedback_message = "Um monstro bloqueia sua passagem! Você precisa lidar com ele primeiro."
            return
        direction_map = {
            'norte': 'north',
            'sul': 'south',
            'leste': 'east',
            'oeste': 'west',
            'cima': 'up',
            'baixo': 'down'
        }
        json_direction = direction_map.get(direction)
        current_room = self.player.current_room

        if json_direction not in current_room.exits:
            self.feedback_message = "Você não pode ir nessa direção."
            return

        next_data = current_room.exits[json_direction]

        # Caso a saída seja trancada
        if isinstance(next_data, dict):
            if next_data.get("locked", False):
                locked_msg = next_data.get("locked_message", "A passagem está trancada.")
                self.feedback_message = locked_msg
                return
            else:
                next_room_name = next_data.get("room")
        else:
            next_room_name = next_data

        next_room_object = self.game_map.get_room(next_room_name)
        if next_room_object:
            self.player.move(next_room_object)
            self.feedback_message = f"Você se moveu para {direction.upper()}."

            if next_room_object.monster:
                monster_name = next_room_object.monster.get("name", "uma criatura desconhecida")
                monster_desc = next_room_object.monster.get("description", "Ela parece perigosa...")
                self.feedback_message += f"\nVocê se depara com {monster_name}! {monster_desc}"
        else:
            self.feedback_message = "Erro no mapa: Sala de destino não encontrada."


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

    def _handle_usar(self, item):
        """Lógica para usar item em uma sala."""
        if item not in self.player.itens:
            self.feedback_message = f"Você não tem '{item}' no seu inventário."
            return
        
        # tenta encontrar uma ação compatível na sala
        action_data = self.player.current_room.get_item_usage(item)
        if not action_data:
            self.feedback_message = f"Você usou o item {item}\nNada aconteceu."
            return

        desc = action_data.get("description", "Você usou o item.")
        action = action_data.get("action", {})
        action_type = action.get("type")

        # processa ação especial
        if action_type == "abrir_direcao":
            direction = action.get("direction")
            target_room = action.get("target_room")
            if direction in self.player.current_room.exits:
                if isinstance(self.player.current_room.exits[direction], dict):
                    # destranca a saída
                    self.player.current_room.exits[direction]["locked"] = False
                    self.player.current_room.exits[direction]["room"] = target_room
                    self.feedback_message = f"{desc}\nA passagem para { self.view._translate_direction(direction)} foi aberta!"
                else:
                    self.feedback_message = f"{desc}\nA passagem já estava aberta."
            else:
                self.feedback_message = f"{desc}\nMas algo parece não funcionar corretamente."
        elif action_type == "remover_item":
            item_to_remove = action.get("item_name")
            if item_to_remove and item_to_remove in self.player.itens:
                self.player.drop_item(item_to_remove)
                self.feedback_message = f"{desc}\nO item '{item_to_remove}' foi removido do seu inventário."
            else:
                self.feedback_message = desc
        else:
            self.feedback_message = desc

    def _display_help(self):
        """Exibe os comandos disponíveis e pausa a tela."""
        help_text = (
            "Comandos disponíveis:\n"
            "  norte, sul, leste, oeste, cima, baixo - Move o jogador.\n"
            "  pegar [item]             - Pega um item da sala.\n"
            "  largar [item]            - Larga um item do inventário.\n"
            "  usar [item]              - Usa um item (pode destrancar algo ou realizar ações).\n"
            "  ajuda                    - Exibe este menu.\n"
            "  sair                     - Encerra o jogo."
        )
        self.view.display_message(help_text)
        self.view.get_command("\nPressione ENTER para voltar ao jogo...")
