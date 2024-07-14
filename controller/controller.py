import requests
import tkinter as tk
from view.gui import LambdaCalcView
from model.lexer import lexer
from model.parser_p import parser, Lambda
from model.evaluator import Logger, evaluate, alpha_convert, eta_reduce, fresh_var
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

class LambdaCalcController:
    def __init__(self, view):
        self.view = view
        self.view.set_eval_button_command(self.evaluate_expression)
        self.view.set_alpha_button_command(self.alpha_convert_expression)
        self.view.set_eta_button_command(self.eta_reduce_expression)

    def evaluate_expression(self) -> None:
        """Evaluate lambda calculus expression."""
        print("Evaluating expression...")
        expression = self.view.get_expression()
        try:
            # Lexical analysis
            print("Lexical analysis...")
            lexer.input(expression)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            self.view.display_tokens(tokens)

            # Parsing
            print("Parsing...")
            ast = parser.parse(expression)
            self.view.display_ast(ast)
            print(f"Parsed AST: {ast}")

            # Evaluation with capturing output
            print("Evaluation with capturing output...")
            logger = Logger()
            try:
                result, logger = evaluate(ast, logger)
                evaluation_steps = logger.get_steps()
                evaluation_steps.append(f"Result: {result}")
                self.view.display_evaluation(evaluation_steps)
                print(f"Evaluation result: {result}")
            except Exception as e:
                print(f"Error during evaluation: {e}")
                self.view.display_error(f"Error during evaluation: {e}")

            # Get explanations from ChatGPT
            print("Getting explanations from ChatGPT...")
            explanations = self.get_chatgpt_explanations(evaluation_steps)
            if explanations:
                self.view.display_explanations(explanations)
                print(f"Explanations: {explanations}")

        except Exception as e:
            print(f"Error: {e}")
            self.view.display_error(f"Error: {e}")

    def alpha_convert_expression(self) -> None:
        """Alpha convert lambda calculus expression."""
        print("Alpha converting expression...")
        expression = self.view.get_expression()
        try:
            # Lexical analysis
            print("Lexical analysis...")
            lexer.input(expression)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            self.view.display_tokens(tokens)

            # Parsing
            print("Parsing...")
            ast = parser.parse(expression)
            self.view.display_ast(ast)
            print(f"Parsed AST: {ast}")

            # Alpha conversion
            print("Alpha conversion...")
            logger = Logger()
            used_vars = {tok.value for tok in tokens if tok.type == 'VAR'}
            new_var = fresh_var(used_vars)
            alpha_converted_ast = alpha_convert(ast, ast.var if isinstance(ast, Lambda) else tokens[0].value, new_var, logger)

            # Display the steps in a cleaner format
            print("Alpha Conversion Steps:")
            alpha_conversion_steps = logger.get_steps()
            for step in alpha_conversion_steps:
                print(step)
            self.view.display_alpha_conversion(alpha_conversion_steps)
            self.view.display_ast(alpha_converted_ast)
            print(f"Alpha converted AST: {alpha_converted_ast}")

            # Get explanations for alpha conversion from ChatGPT
            print("Getting explanations for alpha conversion from ChatGPT...")
            explanations = self.get_chatgpt_explanations(alpha_conversion_steps)
            if explanations:
                self.view.display_explanations(explanations)
                print(f"Explanations: {explanations}")

        except Exception as e:
            print(f"Error: {e}")
            self.view.display_error(f"Error: {e}")

    def eta_reduce_expression(self) -> None:
        """Perform eta reduction on lambda calculus expression."""
        print("Eta reducing expression...")
        expression = self.view.get_expression()
        try:
            # Lexical analysis
            print("Lexical analysis...")
            lexer.input(expression)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            self.view.display_tokens(tokens)

            # Parsing
            print("Parsing...")
            ast = parser.parse(expression)
            self.view.display_ast(ast)
            print(f"Parsed AST: {ast}")

            # Eta reduction
            print("Eta reduction...")
            logger = Logger()
            eta_reduced_ast = eta_reduce(ast, logger)

            # Display the steps in a cleaner format
            print("Eta Reduction Steps:")
            eta_reduction_steps = logger.get_steps()
            if not eta_reduction_steps:
                eta_reduction_steps.append("No eta reduction performed.")
            for step in eta_reduction_steps:
                print(step)
            self.view.display_eta_reduction(eta_reduction_steps)
            self.view.display_ast(eta_reduced_ast)
            print(f"Eta reduced AST: {eta_reduced_ast}")

            # Get explanations for eta reduction from ChatGPT
            print("Getting explanations for eta reduction from ChatGPT...")
            explanations = self.get_chatgpt_explanations(eta_reduction_steps)
            if explanations:
                self.view.display_explanations(explanations)
                print(f"Explanations: {explanations}")

        except Exception as e:
            print(f"Error: {e}")
            self.view.display_error(f"Error: {e}")

    def get_chatgpt_explanations(self, steps):
        """Get explanations from ChatGPT."""
        url = f"https://{RAPIDAPI_HOST}/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {RAPIDAPI_KEY}',
            'X-RapidAPI-Host': RAPIDAPI_HOST
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Explain the following steps in lambda calculus: {steps}"}
            ]
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            explanations = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return explanations
        except requests.RequestException as e:
            print(f"Error fetching explanations from ChatGPT: {e}")
            self.view.display_error(f"Error fetching explanations from ChatGPT: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    view = LambdaCalcView(root)
    controller = LambdaCalcController(view)
    root.mainloop()
