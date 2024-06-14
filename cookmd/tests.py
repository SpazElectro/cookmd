import cookmd.cookmd as cookmd
test = cookmd.parse_cookmd

synerr = cookmd.CookMDSyntaxError

# TODO check if there is a more mainstream solution
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

assert test("<!-- hey -->") == [
    {
        "type": "comment",
        "text": "hey"
    }
]

assert test("[Google](https://www.google.com)") == [
    {
        "type": "link",
        "text": "Google",
        "link": "https://www.google.com"
    }
]

assert test("![Egg](egg.png)") == [
    {
        "type": "image",
        "link": "egg.png",
        "alt": "Egg"
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


cookmd._main()

print("All tests passed!")
