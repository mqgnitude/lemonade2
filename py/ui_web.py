class WebUI:
    def format_status(self, state):
        return (
            f"\n=== Y{state.year}/M{state.month} STATUS ===\n"
            f"Cash:      ${state.cash:,.2f}\n"
            f"Inventory: {state.inventory} units\n"
            f"Price:     ${state.price:.2f}\n"
            f"Staff:     {state.employees}\n"
            f"Marketing: ${state.marketing_spend:.2f}\n"
            f"Loan:      ${state.loan_balance:,.2f}\n"
            "========================"
        )
    
    def help_menu(self):
        return (
            "\nCOMMANDS:\n"
            " [p] set price <val>   | [b] buy stock <amt>\n"
            " [m] marketing <val>   | [h] hire / [f] fire\n"
            " [l] loan <amt>        | [r] repay <amt>\n"
            " [n] next turn         | [s] save / [load] load\n"
            " [help] show this menu"
        )