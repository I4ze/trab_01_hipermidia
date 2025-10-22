import json
from .room import Room

class GameMap:
    def __init__(self, filename="mapa.json"):
        self.rooms = {}
        self.start_room_name = None
        self.exit_room_name = None
        self._load_map(filename)

    def _load_map(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            map_data = json.load(file)
        
        self.start_room_name = map_data.get('main')
        self.exit_room_name = map_data.get('exit')
        self.max_itens = map_data.get('max_itens')
        
        for room_name, room_data in map_data.items():
            if room_name not in ['main', 'exit', 'max_itens']:
                description = room_data.get('description')
                itens = room_data.get('itens')
                useItem = room_data.get('use')
                # Direções são as chaves restantes (north, south, east, west)
                exits = {k: v for k, v in room_data.items() if k not in ['description', 'itens']}
                self.rooms[room_name] = Room(room_name, description, exits, itens, useItem)

    def get_room(self, room_name):
        """
        Retorna informações da sala de um mapa
        """
        return self.rooms.get(room_name)

    def get_start_room(self):
        """
        Retorna sala inicial
        """
        return self.rooms.get(self.start_room_name)

    def get_exit_room_name(self):
        """
        Retorna sala final
        """
        return self.exit_room_name