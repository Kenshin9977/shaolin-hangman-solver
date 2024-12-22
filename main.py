import flet as ft

word_codex = {
    "rave": [
        "harpoon",
        "trees",
        "dance",
        "basement",
        "slasher",
        "memories",
        "charms",
        "boat",
        "kevinsmith",
        "fairies",
    ],
    "spaceland": [
        "brute",
        "octonian",
        "rollercoaster",
        "arcade",
        "slide",
        "geyser",
        "zapper",
        "forgefreeze",
        "bumpercars",
    ],
    "disco": [
        "rollerskates",
        "katana",
        "kungfu",
        "nunchucks",
        "dragon",
        "crane",
        "snake",
        "tiger",
        "pamgrier",
        "arthur",
    ],
    "disco2": [
        "disco",
        "ratking",
        "subway",
        "punks",
        "blackcat",
        "pinkcat",
        "inferno",
        "mcintosh",
        "staff",
        "shield",
    ],
    "extinction": [
        "cryptid",
        "drcross",
        "hives",
        "ancestor",
        "breeder",
        "kraken",
        "obelisk",
        "davidarcher",
        "nightfall",
        "samantha",
    ],
    "willard": [
        "shuffle",
        "winonawyler",
        "director",
        "death",
        "redwoods",
        "mephistopheles",
        "sixtymillion",
        "afterlife",
        "spaceland",
        "shaolin",
    ],
    "characters": [
        "werewolfpoets",
        "losangeles",
        "realitytv",
        "beverlyhills",
        "ghetto",
        "broadway",
        "comicbooks",
        "newyork",
        "actors",
        "audition",
    ],
}

# Normalize word_codex to uppercase
word_codex = {k.upper(): [w.upper() for w in v] for k, v in word_codex.items()}


def get_matching_categories(tries: list):
    if not tries or tries == [""]:
        return list(word_codex.keys())
    matching_categories = []
    for category, word_list in word_codex.items():
        if all(any(w.startswith(word) for w in word_list) for word in tries):
            matching_categories.append(category)
    return matching_categories


def get_words_from_categories(categories):
    matching_words = []
    for category in categories:
        matching_words.extend(word_codex.get(category, []))
    return matching_words


def main(page: ft.Page):
    tries = []  # List to store entered letters
    current_prefix = ""  # Current prefix being formed
    possible_categories = get_matching_categories(tries)
    possible_words = get_words_from_categories(possible_categories)

    # Function to update the remaining possible words based on the entered letters
    def update_possible_words():
        nonlocal tries
        possible_categories = get_matching_categories(tries)
        possible_words = get_words_from_categories(possible_categories)
        possible_words_label.value = "Possible words: " + (
            ", ".join(possible_words) if possible_words else "None"
        )
        page.update()

    def update_possible_words_current_try(e):
        nonlocal tries
        dynamic_tries = tries.copy()
        dynamic_tries.append(try_input.value.upper())
        possible_categories = get_matching_categories(dynamic_tries)
        words_cat = get_words_from_categories(possible_categories)
        possible_words = [w for w in words_cat if w.startswith(try_input.value.upper())]
        possible_words_label.value = "Possible words: " + (
            ", ".join(possible_words) if possible_words else "None"
        )
        page.update()

    # Function to handle the letter input and update the current prefix
    def add_try(e):
        nonlocal current_prefix, tries

        # Get the letter entered and update the prefix
        if try_input.value:
            current_try = try_input.value.upper()
            tries.append(current_try)
            current_prefix = "".join(tries)

            # Update the entered letters label
            try_input.value = ""
            entered_letters_label.value = "Entered tries: " + " ".join(tries)
            update_possible_words()

    # Function to reset the game
    def reset_game(e):
        nonlocal tries, current_prefix, possible_words
        tries = []
        current_prefix = ""
        possible_words = [word for words in word_codex.values() for word in words]

        # Update the UI elements
        entered_letters_label.value = "Entered tries: "
        possible_words_label.value = "Possible words: " + ", ".join(possible_words)
        try_input.value = ""
        page.update()

    # Create UI components
    entered_letters_label = ft.Text(value="Previous tries: ", size=14)
    try_input = ft.TextField(
        hint_text="Displayed letter(s)",
        on_change=update_possible_words_current_try,
        width=200,
    )
    add_button = ft.ElevatedButton(text="Add try", on_click=add_try)
    reset_button = ft.ElevatedButton(text="Reset", on_click=reset_game)
    possible_words_label = ft.Text(
        value="Possible words: " + ", ".join(possible_words), size=14
    )

    # Layout for the input and controls
    input_row = ft.Row([try_input, add_button], spacing=10)
    layout = ft.Column(
        [entered_letters_label, input_row, possible_words_label, reset_button],
        spacing=20,
        expand=True,
    )

    # Set up the page title and add the layout
    page.title = "Shaolin hangman solver"
    page.add(layout)


ft.app(target=main)
