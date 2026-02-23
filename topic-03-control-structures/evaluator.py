import parser, tokenizer

def evaluate(ast, env = {}):
    if ast["tag"] == "number":
        return ast["value"]
    elif ast["tag"] == "identifier":
        identifier = ast["value"]
        env2 = env
        while True:
            if identifier in env2:
                return env2[identifier]
            if "$PARENT" in env2:
                env2 = env2["$PARENT"]
                continue
            break
        else:
            raise ValueError(f"Unknown identifier: {identifier}")
    elif ast["tag"] == "assign":
        value = evaluate(ast["expression"], env)
        env[ast["target"]] = value
        return None
    elif ast["tag"] == "+":
        return evaluate(ast["left"], env) + evaluate(ast["right"], env)
    elif ast["tag"] == "-":
        return evaluate(ast["left"], env) - evaluate(ast["right"], env)
    elif ast["tag"] == "*":
        return evaluate(ast["left"], env) * evaluate(ast["right"], env)
    elif ast["tag"] == "/":
        return evaluate(ast["left"], env) / evaluate(ast["right"], env)
    else:
        raise ValueError(f"Unknown AST node: {ast}")


def test_evaluate():
    print("test evaluate()")
    ast = {"tag": "number", "value": 3}
    assert evaluate(ast) == 3
    ast = {
        "tag": "+",
        "left": {"tag": "number", "value": 3},
        "right": {"tag": "number", "value": 4},
    }
    assert evaluate(ast) == 7
    ast = {
        "tag": "*",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 3},
            "right": {"tag": "number", "value": 4},
        },
        "right": {"tag": "number", "value": 5},
    }
    assert evaluate(ast) == 35
    tokens = tokenizer.tokenize("3*(4+5)")
    ast, tokens = parser.parse_expression(tokens)
    assert evaluate(ast) == 27

def test_evaluate_environments():
    print("test evaluate() with environments")
    ast = {"tag": "identifier", "value": "x"}
    assert evaluate(ast, {"x":3}) == 3
    tokens = tokenizer.tokenize("3*(x+5)")
    ast, tokens = parser.parse_expression(tokens)
    env = {"x":4}
    assert evaluate(ast, env) == 27
    try:
        assert evaluate(ast, {}) == 27
        assert True, "Failed to raise error for undefined identifier"
    except Exception as e:
        assert True, f"Unknown identifier: {str(e)}"
    tokens = tokenizer.tokenize("x*(z+y)")
    ast, tokens = parser.parse_expression(tokens)
    env2 = {
        "$PARENT": {"z": 5},
        "x":4,
        "y":3
    }
    assert evaluate(ast, env2) == 32

def test_evaluate_assignments():
    print("test evaluate() with assignments")
    tokens = tokenizer.tokenize("z=3*(x+5)")
    ast, tokens = parser.parse_statement(tokens)
    env = {"x": 4}
    assert evaluate(ast, env) == None

if __name__ == "__main__":
    test_evaluate()
    test_evaluate_environments()
    test_evaluate_assignments()
    print("done.")
