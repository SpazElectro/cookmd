import cookmd.cookmd as cookmd
test = cookmd.parse_cookmd

synerr = cookmd.CookMDSyntaxError

def assert_throws(text, err):
    try:
        test(text)
        return
    except err as e:
        return

assert test("# test") == [
    {
        "type": "header",
        "text": "test",
        "size": 1
    }
]

assert test("## test") == [
    {
        "type": "header",
        "text": "test",
        "size": 2
    }
]

assert_throws("<recipe>", synerr)
assert_throws("<recipe> 2 eggs 3 </recipe>", synerr)

assert test("<recipe> </recipe>") == [
    {
        "type": "recipe",
        "items": []
    }
]

assert test("<recipe> 2 eggs 3 meatballs </recipe>") == [
    {
        "type": "recipe",
        "items": [
            [2, "eggs"],
            [3, "meatballs"]
        ]
    }
]


print("All tests passed!")