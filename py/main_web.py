import js
from py.game_engine import Engine
from py.ui_web import WebUI
from py.save_manager import SaveManager
from py.tutorial import get_tip

class WebGame:
    def __init__(self):
        self.engine = Engine("Medium")
        self.ui = WebUI()
        self.saver = SaveManager()
    def start(self):
        self.print_to_html(self.ui.help_menu())
        self.print_to_html(self.ui.format_status(self.engine.state))
    def print_to_html(self, text):
        js.window.addToTerminal(text)
    def clear_html(self):
        js.window.clearTerminal()
    def process_input(self, command_str):
        parts = command_str.split()
        if not parts: return
        cmd = parts[0].lower()
        args = parts[1:]
        try:
            if cmd in ['p', 'price']:
                if args:
                    self.engine.state.price = float(args[0])
                    self.print_to_html(f"Price set to ${self.engine.state.price}")
                else: self.print_to_html("Usage: price <value>")
            elif cmd in ['b', 'buy']:
                if args:
                    amt = int(args[0])
                    success, msg = self.engine.buy_inventory(amt)
                    self.print_to_html(msg)
                else: self.print_to_html("Usage: buy <amount>")
            elif cmd in ['m', 'marketing']:
                if args:
                    self.engine.state.marketing_spend = float(args[0])
                    self.print_to_html(f"Marketing set to ${self.engine.state.marketing_spend}")
                else: self.print_to_html("Usage: marketing <value>")
            elif cmd in ['h', 'hire']:
                self.print_to_html(self.engine.hire_employee())
            elif cmd in ['f', 'fire']:
                self.print_to_html(self.engine.fire_employee())
            elif cmd in ['l', 'loan']:
                val = float(args[0]) if args else 1000.0
                self.print_to_html(self.engine.take_loan(val))
            elif cmd in ['r', 'repay']:
                val = float(args[0]) if args else 1000.0
                success, msg = self.engine.repay_loan(val)
                self.print_to_html(msg)
            elif cmd in ['n', 'next']:
                self.clear_html()
                self.engine.process_turn()
                self.print_to_html("\n--- MONTHLY REPORT ---")
                for log in self.engine.state.last_turn_log:
                    self.print_to_html(f" > {log}")
                self.print_to_html(f"\n PROFESSOR SAYS: {get_tip('cash')}")
                self.print_to_html(self.ui.format_status(self.engine.state))
            elif cmd in ['save']:
                json_str = self.saver.save_to_json(self.engine.state)
                js.localStorage.setItem('savegame', json_str)
                self.print_to_html("Game saved to Browser Storage.")
            elif cmd in ['load']:
                json_str = js.localStorage.getItem('savegame')
                if json_str:
                    self.engine.state = self.saver.load_from_json(json_str)
                    self.print_to_html("Game Loaded!")
                    self.print_to_html(self.ui.format_status(self.engine.state))
                else:
                    self.print_to_html("No save found.")
            elif cmd in ['help', '?']:
                self.print_to_html(self.ui.help_menu())
            else:
                self.print_to_html("Unknown command. Type 'help'.")
        except ValueError:
            self.print_to_html("Error: Please check your numbers.")
        except Exception as e:
            self.print_to_html(f"Error: {str(e)}")