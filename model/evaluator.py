import random
import string
from model.parser_p import Lambda, Var, App, Num

# Depth limit to avoid infinite recursion
DEPTH_LIMIT = 100

class Logger:
    def __init__(self):
        self.steps = []

    def log(self, message):
        self.steps.append(message)

    def get_steps(self):
        return self.steps

def fresh_var(used_vars):
    """Generate a fresh variable name not in used_vars."""
    available_vars = list(string.ascii_lowercase + string.ascii_uppercase)
    for var in used_vars:
        if var in available_vars:
            available_vars.remove(var)
    if not available_vars:
        raise Exception("Ran out of fresh variables")
    return random.choice(available_vars)

def alpha_convert(expr, old_var, new_var, logger, top_level=True):
    """Perform alpha conversion by renaming variables."""
    if isinstance(expr, Var):
        result = Var(new_var) if expr.name == old_var else expr
    elif isinstance(expr, Lambda):
        if expr.var == old_var:
            result = Lambda(new_var, alpha_convert(expr.body, old_var, new_var, logger, top_level=False))
        else:
            result = Lambda(expr.var, alpha_convert(expr.body, old_var, new_var, logger, top_level=False))
    elif isinstance(expr, App):
        result = App(alpha_convert(expr.func, old_var, new_var, logger, top_level=False), alpha_convert(expr.arg, old_var, new_var, logger, top_level=False))
    elif isinstance(expr, Num):
        result = expr
    else:
        result = expr

    if top_level and old_var != new_var:  # Log only if there's a change at the top level
        logger.log(f"Alpha Conversion: {old_var} -> {new_var} in {expr} = {result}")
    return result

def substitute(body, var, value, logger):
    """Substitute occurrences of var in body with value."""
    if isinstance(body, Var):
        result = value if body.name == var else body
    elif isinstance(body, Lambda):
        if body.var == var:
            result = body  # Shadowing prevents substitution
        else:
            if body.var in free_vars(value):
                new_var = fresh_var(free_vars(body) | free_vars(value))
                body = alpha_convert(body, body.var, new_var, logger)
            result = Lambda(body.var, substitute(body.body, var, value, logger))
    elif isinstance(body, App):
        result = App(substitute(body.func, var, value, logger), substitute(body.arg, var, value, logger))
    elif isinstance(body, Num):
        result = body
    else:
        result = body

    logger.log(f"Substitute: {var} in {body} with {value} = {result}")
    return result

def free_vars(expr):
    """Return the set of free variables in an expression."""
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Lambda):
        return free_vars(expr.body) - {expr.var}
    elif isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
    return set()

def beta_reduce(expr, logger):
    """Perform beta reduction."""
    if isinstance(expr, App) and isinstance(expr.func, Lambda):
        logger.log(f"Performing Beta Reduction: ({expr.func}) ({expr.arg})")
        return substitute(expr.func.body, expr.func.var, expr.arg, logger)
    return expr

def eta_reduce(expr, logger):
    """Perform eta reduction."""
    if expr is None or logger is None:
        raise ValueError("Input parameters cannot be None.")
    
    if isinstance(expr, Lambda):
        if expr.body is not None and isinstance(expr.body, App) and expr.body.arg is not None and isinstance(expr.body.arg, Var) and expr.body.arg.name == expr.var:
            if not occurs_free(expr.body.func, expr.var):
                logger.log(f"Performing Eta Reduction: {expr}")
                return expr.body.func
    return expr

def occurs_free(expr, var):
    """Check if var occurs free in expr."""
    if isinstance(expr, Var):
        return expr.name == var
    elif isinstance(expr, Lambda):
        if expr.var == var:
            return False
        return occurs_free(expr.body, var)
    elif isinstance(expr, App):
        return occurs_free(expr.func, var) or occurs_free(expr.arg, var)
    return False

def is_normal_form(expr):
    """Check if the expression is in normal form."""
    if isinstance(expr, Var) or isinstance(expr, Num):
        return True
    elif isinstance(expr, Lambda):
        return is_normal_form(expr.body)
    elif isinstance(expr, App):
        return not isinstance(expr.func, Lambda) and is_normal_form(expr.func) and is_normal_form(expr.arg)
    return False

def is_recursive_comb(expr):
    """Check for self-application patterns like the Y combinator."""
    if isinstance(expr, App):
        if isinstance(expr.func, Lambda):
            if isinstance(expr.arg, Lambda):
                if isinstance(expr.arg.body, App):
                    if expr.arg.body.arg == expr.arg:
                        return True
    return False

def evaluate(expr, logger=None, depth=0, perform_alpha_conversion=False):
    """Evaluate the expression by performing reductions until normal form is reached."""
    if logger is None:
        logger = Logger()

    if depth > DEPTH_LIMIT:
        logger.log("Depth limit reached. This expression cannot be reduced to a normal form.")
        return expr, logger

    logger.log(f"Evaluating: {expr}")

    if is_recursive_comb(expr):
        logger.log("Detected a recursive combinator (e.g., Y combinator). This expression may not reduce to a normal form.")
        return expr, logger

    while not is_normal_form(expr):
        new_expr = beta_reduce(expr, logger)
        if new_expr != expr:
            expr = new_expr
            continue
        new_expr = eta_reduce(expr, logger)
        if new_expr != expr:
            expr = new_expr
            continue
        if isinstance(expr, App):
            expr.func, logger = evaluate(expr.func, logger, depth + 1)
            expr.arg, logger = evaluate(expr.arg, logger, depth + 1)
        elif isinstance(expr, Lambda):
            expr.body, logger = evaluate(expr.body, logger, depth + 1)

    # If in normal form and alpha conversion is requested, perform it
    if is_normal_form(expr) and perform_alpha_conversion:
        used_vars = free_vars(expr)
        expr, logger = perform_alpha_conversion_on_normal_form(expr, used_vars, logger)
    
    logger.log(f"Final result: {expr}")
    return expr, logger

def perform_alpha_conversion_on_normal_form(expr, used_vars, logger):
    """Perform alpha conversion on a normal form expression."""
    if isinstance(expr, Lambda):
        new_var = fresh_var(used_vars)
        used_vars.add(new_var)
        expr = alpha_convert(expr, expr.var, new_var, logger)
        expr.body, logger = perform_alpha_conversion_on_normal_form(expr.body, used_vars, logger)
    elif isinstance(expr, App):
        expr.func, logger = perform_alpha_conversion_on_normal_form(expr.func, used_vars, logger)
        expr.arg, logger = perform_alpha_conversion_on_normal_form(expr.arg, used_vars, logger)
    return expr, logger

# # Example usage
# if __name__ == "__main__":
#     logger = Logger()
#     expression = "((((#f.(#g.(#x.((f x) (g x)))))(#m.(#n.(n m))))(#n.z))p)"

#     # Lexical analysis
#     lexer.input(expression)
#     tokens = []
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         tokens.append(tok)

#     # Parsing
#     ast = parser.parse(expression)
#     print(f"Parsed AST: {ast}")

#     # Evaluation with capturing output
#     result, logger = evaluate(ast, logger)

#     evaluation_steps = logger.get_steps()
#     for step in evaluation_steps:
#         print(step)

#     print(f"Final result: {result}")
