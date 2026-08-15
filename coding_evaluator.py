import ast
import re


def evaluate_coding_response(response):
    code_match = re.search(
        r"```python\s*(.*?)```",
        response,
        re.DOTALL | re.IGNORECASE
    )

    if not code_match:
        return False

    code = code_match.group(1)

    try:
        tree = ast.parse(code)

        function_nodes = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "square"
        ]

        if not function_nodes:
            return False

        function_tree = ast.Module(
            body=[function_nodes[0]],
            type_ignores=[]
        )

        compiled_code = compile(
            function_tree,
            "<model_code>",
            "exec"
        )

        namespace = {}

        exec(
            compiled_code,
            {"__builtins__": {}},
            namespace
        )

        square = namespace.get("square")

        if not callable(square):
            return False

        tests = [
            (4, 16),
            (-5, 25),
            (8.5, 72.25)
        ]

        for value, expected in tests:
            result = square(value)

            if result != expected:
                return False

        return True

    except Exception:
        return False