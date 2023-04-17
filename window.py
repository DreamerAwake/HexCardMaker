from tkinter import Tk, IntVar, StringVar, Text, END
from tkinter import Label as tkLabel
from tkinter.ttk import Button, Entry, Frame, Label, OptionMenu, Checkbutton
from PIL import ImageTk

import card_visualizer
import hexcard


class MainTkWindow:
    """Contains all of the TkInter objects in the window."""
    def __init__(self):
        self.window = init_tk_window()
        self.content_frame = init_content_frame(self.window)

        # Create the labels and put them in the frame
        init_labels(self.content_frame)

        # Initialize the title entry variable and widget
        self.title_variable = StringVar()
        init_title_entry(self.content_frame, self.title_variable)

        # Initialize the Hex Type Dropdowns
        self.type_variables = (StringVar(), StringVar(), StringVar(), StringVar())
        init_drop_downs(self.content_frame, self.type_variables)

        # Initialize the Rulebox extender Checkbox
        self.extend_rules = IntVar()
        init_checkboxes(self.content_frame, self.extend_rules)

        # Initialize the flavor text widget
        self.rules_text = init_text_widget(self.content_frame,
                                           ('Arial', 10),
                                           column=2, row=4, columnspan=4, sticky="nsew")
        self.flavor_text = init_text_widget(self.content_frame,
                                            ('Arial', 10, 'italic'),
                                            column=2, row=6, columnspan=4, sticky="nsew")

        # Create the generate button
        init_generate_button(self.content_frame)

        # Create the image of the card
        self.displayed_image_label, self.displayed_image = init_displayed_image(self.content_frame)


def init_tk_window():
    """Initializes a tkinter Tk, returns it."""
    window_frame = Tk()
    window_frame.title("HexCard Maker v0.0")
    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=1)

    window_frame.minsize(1100, 600)

    return window_frame


def init_checkboxes(parent, variable):
    """Creates the checkboxes in the window."""
    extend_rules_checkbox = Checkbutton(parent, text="(This will override the flavor text)" , variable=variable, onvalue=1, offvalue=0)
    extend_rules_checkbox.grid(column=2, row=5, columnspan=4, sticky="w")


def init_content_frame(window):
    """Creates the empty content frame used as the master frame for other widgets."""
    content_frame = Frame(window, padding=20)
    content_frame.grid(column=0, row=0, sticky="nsew")

    # Configure column weights
    content_frame.columnconfigure(1, weight=1)
    content_frame.columnconfigure(2, weight=2)
    content_frame.columnconfigure(3, weight=2)
    content_frame.columnconfigure(4, weight=2)
    content_frame.columnconfigure(5, weight=2)
    content_frame.columnconfigure(6, weight=10)

    # Configure row weights
    content_frame.rowconfigure(4, weight=1)
    content_frame.rowconfigure(6, weight=1)

    return content_frame


def init_displayed_image(parent, image=None):
    """Creates the displayed image label and returns it with a basic placeholder image inside.
    May accept an ImageTK for display."""
    if image is None:
        image = ImageTk.PhotoImage(card_visualizer.generate_hexmask())
    else:
        image = image

    image_label = tkLabel(parent, image=image)
    image_label.grid(column=6, row=1, rowspan=7)

    return image_label, image


def init_drop_downs(parent, variables):

    # Sets the first column to get a dropdown box, shouldn't be changed unless everything else moves
    start_at_column = 2

    for string_var in variables:
        # Creates the drop down for this variable
        this_menu = OptionMenu(parent, string_var, hexcard.HEXTYPES[0], *hexcard.HEXTYPES)
        this_menu.grid(column=start_at_column, row=2)
        start_at_column += 1


def init_generate_button(parent):
    generate_button = Button(parent, text="Make HexCard", command=submit_to_card_visualizer)
    generate_button.grid(column=2, row=7, columnspan=4)


def init_labels(parent):
    """Creates the labels for the content."""
    # Create the Title Label
    title_label = Label(parent, text="HexCard Maker", font=("Times New Roman", 24, 'bold'))
    title_label.grid(column=0, row=0, columnspan=7)

    # Create Entry Labels
    entry_hexcard_label = Label(parent, text="Hex Title:")
    entry_hexcard_label.grid(column=1, row=1)

    entry_hextypes_label = Label(parent, text="Hex Types:")
    entry_hextypes_label.grid(column=1, row=2)

    entry_hexrules_label = Label(parent, text="Hex Rules Text:")
    entry_hexrules_label.grid(column=1, row=4)

    extend_hexrules_label = Label(parent, text="Extend Rules Textbox:")
    extend_hexrules_label.grid(column=1, row=5)

    entry_hexflavor_label = Label(parent, text="Hex Flavor Text:")
    entry_hexflavor_label.grid(column=1, row=6)


def init_text_widget(parent, font, **kwargs):
    """Creates the flavor text input widget"""
    text_widget = Text(parent, width=40, height=6, wrap="word", font=font)
    text_widget.grid(**kwargs)

    return text_widget


def init_title_entry(parent, variable):
    """Create the entry widgets and return them."""
    title_entry = Entry(parent, width=40, textvariable=variable, font=('Arial', 12, 'bold'))
    title_entry.grid(column=2, row=1, columnspan=4)


def print_window_size():
    print(main_window.window.winfo_width(), main_window.window.winfo_height())


def submit_to_card_visualizer():
    """Writes the current stats to the hexcard, then submits that card to the visualizer."""
    print_window_size()
    write_to_hexcard()

    main_window.displayed_image_label, main_window.displayed_image = \
        init_displayed_image(main_window.content_frame, ImageTk.PhotoImage(card_visualizer.generate_hexcard_image(displayed_hexcard, main_window)))

def write_to_hexcard():
    """Writes the data from the boxes into the current hexcard."""
    # Get the Hextypes
    hextypes = []

    for string_var in main_window.type_variables:
        this_type = string_var.get()
        if this_type != "[NONE]":
            hextypes.append(this_type)

    hextypes = tuple(hextypes)

    # Set the hexcard to the current values of the entries
    displayed_hexcard.hex_title = main_window.title_variable.get()
    displayed_hexcard.hex_types = hextypes
    displayed_hexcard.hex_flavor_text = main_window.flavor_text.get("1.0", END)
    displayed_hexcard.hex_rules_text = main_window.rules_text.get("1.0", END)

    print(displayed_hexcard)


# Creates a global variable window
main_window = MainTkWindow()

# Creates global hexcard variable
displayed_hexcard = hexcard.get_blank_hexcard()


if __name__ == "__main__":
    main_window.window.mainloop()

