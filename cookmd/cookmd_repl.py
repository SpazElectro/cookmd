import json
import cookmd.cookmd as cookmd

def get_input() -> str:
    inp = input("> ")
    if inp.endswith("\\"):
        inp = inp[:-1]
        inp += ("\n" + get_input())
    return inp

while True:
    inp = get_input()
    
    if inp == "exit()":
        break

    try:
        out = json.dumps(cookmd.parse_cookmd(
            inp
        ), indent=4)
    except cookmd.CookMDSyntaxError as e:
        out = f"{str(e)}"

    print(out)