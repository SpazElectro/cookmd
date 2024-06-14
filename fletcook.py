# the middleware to convert the data to flet components
import json
import flet as ft
import cookmd.cookmd as cookmd
import webbrowser

DEFAULT_TEXT_SIZE = 12
DEFAULT_ITEMS = {
    # "id": {
    #     "name": "",
    #     "image": "",
    # }
    "egg": {
        "name": "Egg",
        "image": "./default/egg.png"
    },
    "sugar": {
        "name": "Sugar",
        "image": "./default/sugar.png"
    },
    "milk": {
        "name": "Milk",
        "image": "./default/milk.png"
    }
}

def link_click(e: ft.ControlEvent, url: str):
    webbrowser.open(url)


def cookmd_to_flet(page: ft.Page, cook):
    out = []
    items = DEFAULT_ITEMS
    recipe = []

    for e in cook:
        if e["type"] == "comment":
            continue
        # metadata
        elif e["type"] == "extension":
            if e["name"] == "meta":
                if e["data"].get("title", None):
                    page.title = e["data"]["title"]
            elif e["name"] == "item":
                items[e["data"]["id"]] = e["data"]
            else:
                print(f"Unknown extension name: {e['name']}")
        elif e["type"] == "recipe":
            for itm in e["items"]:
                recipe.append({
                    "count": itm[0],
                    "id": itm[1],

                    "name": items[itm[1]]["name"],
                    "image": items[itm[1]]["image"]
                })
            
            print("Secret KFC recipe acquired!")
        # text
        elif e["type"] == "header" or e["type"] == "text":
            out.append(
                ft.Text(e["text"], size=24 - (e.get("size") or 24 - DEFAULT_TEXT_SIZE))
            )
        elif e["type"] == "link":
            lk = e["link"]

            out.append(ft.TextButton(e["text"], on_click=lambda ev: link_click(ev, lk)))
        elif e["type"] == "image":
            out.append(ft.Image(src=e["link"], tooltip=e["alt"]))
        else:
            print(f"Unknown element type: {e['type']}")

    return (out, recipe)
