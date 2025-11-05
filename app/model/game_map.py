import json
from .room import Room

class GameMap:
    def __init__(self, filename="mapa.json"):
        self.rooms = {}
        self.start_room_name = None
        self.exit_room_name = None
        self.max_itens = 2  # valor default
        self._load_map(filename)

    def _load_map(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            map_data = json.load(file)
        
        # Campos principais
        self.start_room_name = map_data.get('main')
        self.exit_room_name = map_data.get('exit')
        self.max_itens = map_data.get('max_itens', 2)

        rooms_data = map_data.get('rooms', {})
        
        for room_name, room_data in rooms_data.items():
            description = room_data.get('description', "")
            itens = room_data.get('itens', {})
            useItem = room_data.get('use', [])
            monster = room_data.get('monster', None)

            # Tratamento das saídas (north, south, etc.)
            exits = {}
            for direction, value in room_data.items():
                if direction in ["description", "itens", "use", "monster"]:
                    continue
                
                # Caso simples: string → destino direto
                if isinstance(value, str):
                    exits[direction] = {
                        "room": value,
                        "locked": False,
                        "key_item": None,
                        "locked_message": None
                    }
                # Caso complexo: objeto com dados de tranca
                elif isinstance(value, dict):
                    exits[direction] = {
                        "room": value.get("room"),
                        "locked": value.get("locked", False),
                        "key_item": value.get("key_item"),
                        "locked_message": value.get("locked_message")
                    }

            self.rooms[room_name] = Room(
                name=room_name,
                description=description,
                exits=exits,
                itens=itens,
                useItem=useItem,
                monster=monster
            )

    def get_room(self, room_name):
        """Retorna uma sala específica do mapa"""
        return self.rooms.get(room_name)

    def get_start_room(self):
        """Retorna a sala inicial"""
        return self.rooms.get(self.start_room_name)

    def get_exit_room_name(self):
        """Retorna o nome da sala final"""
        return self.exit_room_name
