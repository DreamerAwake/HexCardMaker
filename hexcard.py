from dataclasses import dataclass


HEXTYPES = (
    "[NONE]",
    "Desert",
    "Farm",
    "Field",
    "Forest",
    "Hill",
    "River",
    "Road",
    "Sea",
    "Settlement",
    "Snow",
    "Swamp"
)


@dataclass
class HexCard:
    """Contains information about a HexCard.
    Starts out blank and is filled with info aggregated from the TKInter window."""
    hex_title: str
    hex_types: tuple

    hex_flavor_text: str
    hex_rules_text: str



def get_blank_hexcard():
    """Returns a 'blank' HexCard object."""
    return HexCard("", (), "", "")