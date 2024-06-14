# the application that shows the cook md file and allows you to search add remove
from typing import TypedDict
import cookmd.cookmd as cookmd
import fletcook
import flet as ft

class Ingredient(TypedDict):
    # {'count': 5, 'id': 'egg', 'name': 'Egg', 'image': 'egg.png'}
    count: int
    id: str
    name: str
    image: str

def controls(page: ft.Page):
    meal = fletcook.cookmd_to_flet(page, cookmd.parse_cookmd(open("test.cookmd").read()))
    page.add(*meal[0])

    recipe = meal[1]
    for ingredient in recipe:
        ingredient: Ingredient = ingredient
        page.add(
            ft.Card(
                ft.Container(
                    ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Image(ingredient["image"]),
                                title=ft.Text(str(ingredient["count"]) + " " + ingredient["name"] + "(s)"),
                                subtitle=ft.Text(ingredient["id"]),
                                trailing=ft.Icon(ft.icons.CHECK_BOX_OUTLINE_BLANK),
                            ),
                            ft.Row(
                                [
                                    ft.TextButton("Mark as done"),
                                    ft.TextButton("Mark as absent")
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            )            
        )

def main(page: ft.Page):
    def onkeypress(e: ft.KeyboardEvent):
        if e.key == "F5":
            print("updating page")
            for _ in range(len(page.controls)): # type: ignore
                page.controls.pop() # type: ignore
            page.update()
            controls(page)
            page.update()
    page.scroll = ft.ScrollMode.ALWAYS
    page.on_keyboard_event = onkeypress
    controls(page)

ft.app(main)