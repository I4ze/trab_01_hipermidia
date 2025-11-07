import os

class GameView:
    """
    View do jogo. Responsável por toda a entrada (input) e saída (output).
    """
    
    def display_message(self, message):
        """Exibe uma mensagem simples para o usuário."""
        print(f"\n{message}")

    def display_room(self, room, previous_room=None):
        """
        Exibe as informações detalhadas da sala atual:
        - Nome e descrição.
        - Sala anterior (se houver).
        - Saídas disponíveis.
        - Itens na sala.
        """
        print("\n" + "=" * 50)
        print(f"Local atual: {room.name}")
        if previous_room:
            print(f"Sala anterior: {previous_room.name}")
        print("=" * 50)

        # Descrição da Sala
        print(f"{room.description}")

        # Saídas
        if room.exits:
            exits_list = []
            for direction, target_room in room.exits.items():
                # converte 'north' para 'norte' (para display)
                display_dir = self._translate_direction(direction)

                # caso a saída seja um dicionário (porta trancada, etc)
                if isinstance(target_room, dict):
                    target_name = target_room.get("room", "???")
                    locked = target_room.get("locked", False)
                    if locked:
                        exits_list.append(f"{display_dir.capitalize()} (trancada)")
                    else:
                        exits_list.append(f"{display_dir.capitalize()} -> {target_name.capitalize()}")
                else:
                    exits_list.append(f"{display_dir.capitalize()} -> {target_room.capitalize()}")

            print(f"\nSaídas: {', '.join(exits_list)}")
        else:
            print("\nVocê está preso!")

        # Itens na Sala
        if room.itens:
            itens_list = [f"{name} ({description})" for name, description in room.itens.items()]
            print(f"Itens na sala: {', '.join(itens_list)}")
        else:
            print("Não há itens aqui.")


    def display_inventory(self, inventory):
        """Exibe o inventário do jogador."""
        print("-" * 50)
        if inventory:
            itens_list = [f"{name} ({description})" for name, description in inventory.items()]
            print(f"Você tem: {', '.join(itens_list)}")
        else:
            print("Seu inventário está vazio")
        print("-" * 50)

    def get_command(self, prompt="O que você faz? > "):
        """
        Lê a entrada do usuário e retorna o comando.
        Aceita um prompt opcional (como "Pressione ENTER...").
        """
        return input(prompt).strip()

    def _translate_direction(self, direction):
        """
        Função auxiliar para traduzir direções do inglês para o português.
        """
        translation = {
            'north': 'norte',
            'south': 'sul',
            'east': 'leste',
            'west': 'oeste',
            'up': 'cima',
            'down': 'baixo',
        }
        return translation.get(direction, direction)
    
    def clear_terminal(self):
        """Limpa o terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

