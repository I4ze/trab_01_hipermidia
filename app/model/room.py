class Room:
    def __init__(self, name, description, exits, items):
        self.name = name
        self.description = description
        self.exits = exits # {'north': 'sala de musica', ...}
        self.items = items # {'faca': 'faca ornamental sem fio', ...}
    
    def get_item(self, item_name):
        """
        Remove item da sala
        """
        return self.items.pop(item_name, None)
    
    def add_item(self, item_name, item_description):
        """
        Adiciona item na sala
        """
        self.items[item_name] = item_description
        
        