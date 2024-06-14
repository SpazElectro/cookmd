# TODO add more ways to trigger this
class CookMDSyntaxError(RuntimeError):
    pass


# read_until("epic gaming >", ">") -> "epic gaming "
def read_until(text, seperator) -> str:
    out = ""
    for x in text:
        if x == seperator:
            break
        out += x
    return out


# read_until_exclude("##hey", "#") -> "hey"
def read_until_exclude(text, exclude) -> str:
    out = ""
    for x in text:
        if x != exclude:
            break
        out += x
    return out


# read_until_next_line("hey!\nwhat's up!") -> "hey!"
def read_until_next_line(text) -> str:
    return read_until(text, "\n")


def parse_extension_data(data: str) -> dict[str, str]:
    # data:
    # title="Test cook"
    # return {"title": "Test cook"}
    output = {}
    ineq = False
    instr = False
    name = ""
    value = ""
    string_character = ""
    previous_character = ""

    for char in data:
        if char == "=":
            ineq = True
            continue
        if (char == '"' or char == "'") and previous_character != "\\":
            if string_character == "":
                string_character = char
            if char == string_character:
                instr = not instr
                if ineq and not instr:
                    output[name.strip()] = value.strip()
                    name = ""
                    value = ""
                    ineq = False
                    instr = False
                if not instr:
                    string_character = ""
                continue
        
        if char != "\\":
            if ineq:
                value += char
            else:
                name += char
        previous_character = char

    if name != "" or value != "":
        raise CookMDSyntaxError(
            'Syntax error: Extension data is incorrect! example usage: <element name="abc"> (quotes are mandatory!)'
        )

    return output


def parse_cookmd(text: str):
    output = []

    line_number = 0
    line = ""

    previous_character = "\n"
    character_index = 0

    saved_lines = []
    save_lines = False

    done = False
    done_line = False
    for character in text:
        text_left = text[character_index:]
        next_character = text_left[1:2]
        line = read_until_next_line(text_left)
        full_line = text.splitlines()[line_number]
        if save_lines:
            done = True
            if not (
                full_line.strip() == ""
                or full_line.strip() == "<recipe>"
                or full_line.strip() == "</recipe>"
            ):
                k = [
                    int(full_line.strip().split(" ")[0]),
                    full_line.strip().split(" ")[1],
                ]
                if not k in saved_lines:
                    saved_lines.append(k)

        if character == "\n":
            line_number += 1
        if previous_character == "\n":
            done = False
            done_line = False
            if character == "#":
                size = len(read_until_exclude(text_left, "#"))

                output.append(
                    {"type": "header", "text": line[size:].strip(), "size": size}
                )
                done = True
            elif character == "[":
                link_text = read_until(text_left, "]")

                output.append(
                    {
                        "type": "link",
                        "text": link_text[1:].strip(),
                        "link": read_until(text_left[len(link_text) + 2 :], ")"),
                    }
                )
                done = True
            elif character == "!":
                if next_character == "[":
                    image_alt = read_until(line[2:], "]")

                    output.append(
                        {
                            "type": "image",
                            "link": read_until(line[len(image_alt) + 4 :], ")"),
                            "alt": image_alt,
                        }
                    )
                    done = True
        if character == "<":
            line = line.strip()
            if not full_line.endswith(">"):
                raise CookMDSyntaxError(
                    'Syntax error: Extension did not end with a ">"'
                )

            if line.startswith("<!--"):
                output.append(
                    {
                        "type": "comment",
                        "text": line[4 : len(read_until(line, "-->")) - 3].strip(),
                    }
                )

                done = True
            else:
                data = read_until(line[1:], ">")
                extension = read_until(data, " ")
                data = parse_extension_data(" ".join(data.split(" ")[1:]))

                if extension == "/recipe":
                    # this is the END of an extension define
                    # this only occurs for the recipe as of now
                    if save_lines:
                        save_lines = False
                        output.append({"type": "recipe", "items": saved_lines})
                elif extension == "recipe":
                    save_lines = not "</recipe>" in line
                    recipe_contents = (
                        line.split("<recipe>")[1].split("</recipe>")[0].strip()
                    )
                    if recipe_contents != "":
                        recipe_contents_index = 0
                        amount = 0

                        for item in recipe_contents.split(" "):
                            if recipe_contents_index % 2 == 0:
                                if not item.isdigit():
                                    raise CookMDSyntaxError(
                                        'Syntax error: <recipe> should be used as such: "<recipe>{amount} {item} 3 milk_cartons</recipe>"'
                                    )

                                amount = int(item)
                            else:
                                saved_lines.append([amount, item])
                            recipe_contents_index += 1

                        if recipe_contents_index % 2 == 1:
                            raise CookMDSyntaxError(
                                "Syntax error: unfinished element in <recipe>"
                            )
                    if not save_lines:
                        output.append({"type": "recipe", "items": saved_lines})
                else:
                    output.append(
                        {"type": "extension", "name": extension, "data": data}
                    )

                done = True
        if not done and not done_line and not save_lines:
            if full_line.strip() != "":
                output.append({"type": "text", "text": full_line.strip()})
                done_line = True
        previous_character = character
        character_index += 1

    if save_lines:
        raise CookMDSyntaxError("Syntax error: <recipe> was not closed!")

    return output


def _main():
    import timeit

    cook = open("test.cookmd").read()
    timeit.timeit()
    parsed = parse_cookmd(cook)

    print(f"Parsed file in {timeit.timeit()}s!")
    open("parsed.json", "w").write(__import__("json").dumps(parsed, indent=4))


if __name__ == "__main__":
    _main()