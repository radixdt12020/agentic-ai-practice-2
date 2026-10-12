import ast
import inspect
import pytest
import solution
from solution import collatz_steps


def test_collatz_steps_base():
    assert collatz_steps(1) == 0
    assert collatz_steps(2) == 1
    assert collatz_steps(4) == 2


def test_collatz_steps_6():
    assert collatz_steps(6) == 8


def test_collatz_steps_27():
    assert collatz_steps(27) == 111


def test_collatz_steps_large():
    assert collatz_steps(989345275647) == 1348


def test_ast_constraints():
    source = inspect.getsource(solution)
    tree = ast.parse(source)

    # Verify absence of ast.For, ast.While, ast.AsyncFor
    for node in ast.walk(tree):
        assert not isinstance(node, (ast.For, ast.AsyncFor)), (
            f"Forbidden loop node found: {type(node).__name__}"
        )
        assert not isinstance(node, ast.While), (
            f"Forbidden while node found: {type(node).__name__}"
        )

    # Verify absence of function recursion
    fn_defs = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fn_defs[node.name] = node

    for fn_name, fn_node in fn_defs.items():
        for inner in ast.walk(fn_node):
            if inner is not fn_node and isinstance(inner, ast.Call):
                if isinstance(inner.func, ast.Name) and inner.func.id == fn_name:
                    pytest.fail(f"Forbidden recursion detected: '{fn_name}' calls itself")
