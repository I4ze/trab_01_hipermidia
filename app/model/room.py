import random

class Room:
    def __init__(self, name, description, exits, itens, useItem, monster):
        self.name = name
        self.description = description
        self.exits = exits # {'north': 'sala de musica', ...}
        self.itens = itens # {'faca': 'faca ornamental sem fio', ...}
        self.item_usage = useItem  #[{"item" : "partitura", "description": "alguma coisa curta" ,"action": ? }]
        self.monster = monster
        
        if self.monster:
            self.monster["tentativas"] = random.randint(1, 5)

    def get_item(self, item_name):
        """
        Remove item da sala
        """
        return self.itens.pop(item_name, None)
    
    def add_item(self, item_name, item_description):
        """
        Adiciona item na sala
        """
        self.itens[item_name] = item_description
        
    def get_item_usage(self, item_name):
        for useItem in self.item_usage:
            if useItem["item"] == item_name:
                return useItem
        
        return None
    
    def has_monster(self):
        """Retorna True se há um monstro ativo na sala."""
        return self.monster is not None

    def try_defeat_monster(self, item_name):
        """
        Tenta derrotar o monstro com o item fornecido.
        Retorna uma tupla (derrotou, mensagem, perdeu_jogo).
        """
        if not self.monster:
            return (False, "Não há nenhum monstro aqui.", False)

        monster = self.monster

        # item correto
        if item_name == monster.get("defeat_item"):
            msg = monster.get("defeat_message", f"Você derrotou o {monster['name']}!")
            self.monster = None  # monstro removido
            return (True, msg, False)

        # item incorreto perde tentativa
        monster["tentativas"] -= 1
        if monster["tentativas"] <= 0:
            return (False, f"O {monster['name']} se cansa da batalha e te ataca em um instante com um golpe fatal\nVocê foi morto!", True)
        else:
            return (False, f"O {monster['name']} resistiu ao ataque!", False)