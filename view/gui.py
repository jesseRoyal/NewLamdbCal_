import tkinter as tk
from tkinter import messagebox, scrolledtext

class LambdaCalcView:
    def __init__(self, root):
        self.root = root
        self.root.title("Lambda Calculus Interpreter")
        self.root.geometry("900x700")  # Default size
        self.root.configure(bg="#f0f0f0")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Input frame
        input_frame = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10)
        input_frame.grid(row=0, sticky="ew", padx=10, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        self.expr_label = tk.Label(input_frame, text="Lambda Expression:", font=("Arial", 12), bg="#e0e0e0")
        self.expr_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.expr_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.expr_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.eval_button = tk.Button(input_frame, text="Evaluate", font=("Arial", 12), bg="#007bff", fg="white")
        self.eval_button.grid(row=0, column=2, padx=5, pady=5)

        self.alpha_button = tk.Button(input_frame, text="Alpha Convert", font=("Arial", 12), bg="#28a745", fg="white")
        self.alpha_button.grid(row=0, column=3, padx=5, pady=5)

        self.eta_button = tk.Button(input_frame, text="Eta Reduce", font=("Arial", 12), bg="#ffc107", fg="black")
        self.eta_button.grid(row=0, column=4, padx=5, pady=5)

        self.clear_button = tk.Button(input_frame, text="Clear", font=("Arial", 12), bg="#dc3545", fg="white", command=self.clear_all_fields)
        self.clear_button.grid(row=0, column=5, padx=5, pady=5)

        # Output frame
        output_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
        output_frame.grid(row=1, sticky="nsew", padx=10, pady=10)
        output_frame.grid_rowconfigure(5, weight=1)
        output_frame.grid_columnconfigure(1, weight=1)

        self.tokens_label = tk.Label(output_frame, text="Tokens:", font=("Arial", 12), bg="#f0f0f0")
        self.tokens_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.tokens_text = scrolledtext.ScrolledText(output_frame, height=4, font=("Arial", 12))
        self.tokens_text.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.ast_label = tk.Label(output_frame, text="AST:", font=("Arial", 12), bg="#f0f0f0")
        self.ast_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.ast_text = scrolledtext.ScrolledText(output_frame, height=4, font=("Arial", 12))
        self.ast_text.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.evaluation_label = tk.Label(output_frame, text="Evaluation:", font=("Arial", 12), bg="#f0f0f0")
        self.evaluation_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.evaluation_text = scrolledtext.ScrolledText(output_frame, height=10, font=("Arial", 12))
        self.evaluation_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.explanation_label = tk.Label(output_frame, text="Explanations:", font=("Arial", 12), bg="#f0f0f0")
        self.explanation_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.explanation_text = scrolledtext.ScrolledText(output_frame, height=5, font=("Arial", 12))
        self.explanation_text.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def set_eval_button_command(self, command):
        self.eval_button.config(command=command)

    def set_alpha_button_command(self, command):
        self.alpha_button.config(command=command)

    def set_eta_button_command(self, command):
        self.eta_button.config(command=command)

    def get_expression(self):
        return self.expr_entry.get()

    def display_tokens(self, tokens):
        self.tokens_text.delete(1.0, tk.END)
        for token in tokens:
            self.tokens_text.insert(tk.END, f"{token}\n")

    def display_ast(self, ast):
        self.ast_text.delete(1.0, tk.END)
        self.ast_text.insert(tk.END, repr(ast))

    def display_evaluation(self, evaluation_steps):
        self.evaluation_text.delete(1.0, tk.END)
        for step in evaluation_steps:
            self.evaluation_text.insert(tk.END, f"{step}\n")

    def display_explanations(self, explanations):
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, explanations)

    def display_alpha_conversion(self, steps):
        self.evaluation_text.delete(1.0, tk.END)
        for step in steps:
            self.evaluation_text.insert(tk.END, f"{step}\n")

    def display_eta_reduction(self, steps):
        self.evaluation_text.delete(1.0, tk.END)
        for step in steps:
            self.evaluation_text.insert(tk.END, f"{step}\n")

    def display_error(self, error_message):
        messagebox.showerror("Error", error_message)

    def clear_all_fields(self):
        self.expr_entry.delete(0, tk.END)
        self.tokens_text.delete(1.0, tk.END)
        self.ast_text.delete(1.0, tk.END)
        self.evaluation_text.delete(1.0, tk.END)
        self.explanation_text.delete(1.0, tk.END)
