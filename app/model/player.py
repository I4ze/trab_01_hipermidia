class Player:
    def __init__(self, current_room, max_itens):
        self.current_room = current_room
        self.itens = {}
        self.max_itens = max_itens
    
    def move(self, next_room):
        """Atualiza a sala atual do jogador."""
        self.current_room = next_room
        
    def take_item(self, item_name, item_description):
        """
        Adiciona um item ao inventário, verificando o limite.
        Retorna True se o item foi pego, False caso contrário.
        """
        if len(self.itens) < self.max_itens:
            self.itens[item_name] = item_description
            return True
        else:
            return False
        
        