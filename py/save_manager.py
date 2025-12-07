import json
import os
from py.data_models import GameState

class SaveManager:
    def save_to_json(self, state: GameState) -> str:
        return json.dumps(state.to_dict(), indent=2)

    def load_from_json(self, json_str: str) -> GameState:
        data = json.loads(json_str)
        return GameState.from_dict(data)

    def save_to_file(self, state: GameState, filename: str):
        with open(filename, 'w') as f:
            f.write(self.save_to_json(state))
            
    def load_from_file(self, filename: str) -> GameState:
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            return self.load_from_json(f.read())