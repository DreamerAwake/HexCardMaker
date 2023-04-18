from math import ceil
from PIL import Image, ImageDraw, ImageFont


TITLE_FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
TITLE_FONT_REDUCED = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
RULES_FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 10)
FLAVOR_FONT = ImageFont.truetype("C:/Windows/Fonts/ariali.ttf", 10)


def generate_hexcard_image(hexcard, main_window):
    """Generates and returns an image of a hexcard from the given card's properties."""
    print("Generating Image")
    hexcard_image = load_hex_bg(hexcard.hex_types)

    print("Compositing...")
    hexcard_image.alpha_composite(create_type_label_image(hexcard.hex_types), (0, 104))
    hexcard_image.alpha_composite(create_title_label_image(hexcard.hex_title), (0, 54))

    # Check if the rules box should extend over the flavor text
    if main_window.extend_rules.get() == 1:
        hexcard_image.alpha_composite(create_rules_text_image(hexcard.hex_rules_text, extend_rules=True), (0, 330))
    else:
        hexcard_image.alpha_composite(create_rules_text_image(hexcard.hex_rules_text), (0, 330))
        hexcard_image.alpha_composite(create_flavor_text_image(hexcard.hex_flavor_text), (0, 390))

    # Punch out the shape
    hexcard_image.paste(Image.new("RGBA", (500, 500), (0, 0, 0, 0)), mask=generate_hexmask())

    return hexcard_image


def generate_hexmask():
    hexmask = Image.new("RGBA", (500, 500), (128, 128, 128, 255))
    hexmask_editor = ImageDraw.Draw(hexmask)

    hexmask_editor.regular_polygon((250, 250, 225), n_sides=6, fill=(0, 0, 0, 0))

    # hexmask.save("output/hexmask.png", "PNG")

    return hexmask


def break_into_lines(text_sample, image_editor):
    """Takes a string and breaks it into several lines of text based on length so that it can be easily rendered.
    Also requires a PIL ImageDraw object with its font settings initialized to the font to be checked."""
    # Split the text
    wordlist = text_sample.split()

    single_line = []
    final_lines = []

    # Build each line word by word
    for each_word in wordlist:

        # Respond to newline characters
        if each_word == "/n":
            final_lines.append(" ".join(single_line))
            single_line.clear()

        # If the line is short enough, add the next word
        elif image_editor.textlength(" ".join(single_line) + " " + each_word) < 225:
            single_line.append(each_word)

        # If you have reached the end of a line, add to the final line, and go to the next line
        else:
            final_lines.append(" ".join(single_line))
            single_line.clear()
            single_line.append(each_word)

    final_lines.append(" ".join(single_line))
    print(final_lines)

    return final_lines


def chop_into_halves(text):
    """Takes a string and breaks it into two lines at roughly the midpoint, preferring to be top-heavy.
    Returns a tuple of two strings."""
    wordlist = text.split()

    slicepoint = ceil(len(wordlist) / 2)

    line_1 = " ".join(wordlist[:slicepoint])
    line_2 = " ".join(wordlist[slicepoint:])

    return line_1, line_2


def create_flavor_text_image(flavor_text):
    """Draws the flavor text image."""
    flavor_text_image = Image.new("RGBA", (500, 60), (225, 225, 225, 128))
    label_editor = ImageDraw.Draw(flavor_text_image)
    label_editor.font = FLAVOR_FONT

    flavor_text_lines = break_into_lines(flavor_text, label_editor)

    for each_line_index in range(0, len(flavor_text_lines)):
        label_editor.text((250, 12 + (12 * each_line_index)),
                          flavor_text_lines[each_line_index],
                          fill=(0, 0, 0, 255), anchor="mm")

    return flavor_text_image


def create_rules_text_image(rules_text, extend_rules=False):
    """Draws the rules text image."""
    if extend_rules:
        rules_text_image = Image.new("RGBA", (500, 120), (225, 225, 225, 200))
    else:
        rules_text_image = Image.new("RGBA", (500, 60), (225, 225, 225, 200))

    label_editor = ImageDraw.Draw(rules_text_image)
    label_editor.font = RULES_FONT

    rules_text_lines = break_into_lines(rules_text, label_editor)

    for each_line_index in range(0, len(rules_text_lines)):
        label_editor.text((250, 12 + (12 * each_line_index)),
                          rules_text_lines[each_line_index],
                          fill=(0, 0, 0, 255), anchor="mm")

    return rules_text_image


def create_title_label_image(title_text):
    """Creates the title label for the hexcard image. Returns the image of that label for later compositing."""
    # Create the base image and the editor
    title_label_image = Image.new("RGBA", (500, 50), (220, 200, 20, 100))
    label_editor = ImageDraw.Draw(title_label_image)
    label_editor.font = TITLE_FONT

    # See if the Title is too long for the space
    if label_editor.textlength(title_text) < 225:
        # Draw text as normal
        label_editor.text((250, 25), title_text, fill=(0, 0, 0, 255), anchor="mm")

    else:
        # Draw two lines of smaller text
        title_text_lines = chop_into_halves(title_text)
        label_editor.text((250, 16), title_text_lines[0], fill=(0, 0, 0, 255), font=TITLE_FONT_REDUCED, anchor="mm")
        label_editor.text((250, 36), title_text_lines[1], fill=(0, 0, 0, 255), font=TITLE_FONT_REDUCED, anchor="mm")


    # Draw the bounding lines
    label_editor.line(((0, 1), (500, 1)), fill=(0, 0, 0, 180), width=4)
    label_editor.line(((0, 48), (500, 48)), fill=(0, 0, 0, 180), width=4)

    return title_label_image


def create_type_label_image(hextypes):
    """Creates the types labels for the hexcard image. Returns the image of that label for later compositing."""
    # Create the base image and the editor
    title_label_image = Image.new("RGBA", (500, 25), (190, 150, 20, 220))
    label_editor = ImageDraw.Draw(title_label_image)
    label_editor.font = RULES_FONT

    # Create the Hextype string
    hextype_string = ", ".join(hextypes)

    # Draw text
    label_editor.text((250, 13), hextype_string, fill=(0, 0, 0, 255), anchor="mm")

    return title_label_image


def load_hex_bg(hextypes, filepath="data/img/"):
    """Generates a bg image from the hextypes and the images stored in /data/img. Returns an image."""
    # Set the base color for the hex
    if "Snow" in hextypes:
        bg_image = Image.new("RGBA", (500, 500), (220, 220, 220, 255))  # A white-ish base color for snow
    elif "Desert" in hextypes:
        bg_image = Image.new("RGBA", (500, 500), (235, 200, 135, 255))  # A light tan for sand
    elif "Swamp" in hextypes:
        bg_image = Image.new("RGBA", (500, 500), (30, 70, 40, 255))    # A dark swampy green
    else:
        bg_image = Image.new("RGBA", (500, 500), (90, 160, 30, 255))    # A default field green

    # Composite the images for each type based on optimal layering
    layer_order = ("Hill", "Field", "Farm", "River", "Road", "Desert", "Swamp", "Forest", "Settlement", "Sea")

    for each_type in layer_order:
        if each_type in hextypes:
            bg_image.alpha_composite(Image.open(filepath + each_type + ".png"))

    return bg_image
