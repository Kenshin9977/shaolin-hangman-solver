from collections import defaultdict

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
        "yetieyes",
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

word_codex = {k.upper(): [w.upper() for w in v] for k, v in word_codex.items()}


def get_matching_categories(tries):
    matching_categories = []

    tries_sorted = sorted(tries, key=len, reverse=True)

    for category, word_list in word_codex.items():
        remaining_words = word_list.copy()
        category_matches = True

        for word_prefix in tries_sorted:
            matching_word = next(
                (word for word in remaining_words if word.startswith(word_prefix)), None
            )

            if matching_word:
                remaining_words.remove(matching_word)
            else:
                category_matches = False
                break

        if category_matches:
            matching_categories.append(category)

    return matching_categories


def count_prefixes(strings):
    prefix_count = defaultdict(int)
    for string in strings:
        for i in range(1, len(string) + 1):
            prefix = string[:i]
            prefix_count[prefix] += 1
    return dict(
        sorted(prefix_count.items(), key=lambda item: len(item[0]), reverse=True)
    )


def remove_matching_words(list1, list2):
    prefixes_list1 = count_prefixes(list1)
    prefixes_list2 = count_prefixes(list2)
    words_to_remove = set()

    for prefix in prefixes_list1:
        if prefix in prefixes_list2:
            list1_count_prefix = prefixes_list1[prefix]
            list2_words_matching_prefix = [
                word for word in list2 if word.startswith(prefix)
            ]
            if len(list2_words_matching_prefix) >= list1_count_prefix:
                if list1_count_prefix >= len(list2_words_matching_prefix):
                    words_to_remove.update(
                        list2_words_matching_prefix[:list1_count_prefix]
                    )

    return [word for word in list2 if word not in words_to_remove]


def get_words_from_categories(categories, tries):
    matching_words = []
    if not tries:
        return [w for category in categories for w in word_codex.get(category, [])]
    tries_sorted = sorted(tries, key=len, reverse=True)

    for category in categories:
        category_word = word_codex.get(category).copy()
        matching_words.extend(remove_matching_words(tries_sorted, category_word))
    return matching_words


def get_wyler_image(letter):
    if not letter.isalpha():
        return None
    filename = f"{letter.upper()}_Wyler.png"
    return filename


def main(page: ft.Page):
    tries = []
    current_prefix = ""
    possible_categories = get_matching_categories(tries)
    possible_words = get_words_from_categories(possible_categories, tries)

    def update_possible_words():
        nonlocal tries
        possible_categories = get_matching_categories(tries)
        possible_words = get_words_from_categories(possible_categories, tries)
        possible_words_label.value = "Possible words: " + (
            ", ".join(possible_words) if possible_words else "None"
        )
        page.update()

    def translate_to_wyler(e):
        input_text = translate_input.value.upper()
        translation_images.controls.clear()

        for char in input_text:
            img_path = get_wyler_image(char)
            if img_path:
                translation_images.controls.append(
                    ft.Image(src=img_path, width=50, height=50)
                )
            else:
                translation_images.controls.append(ft.Text(f"[{char}]"))

        page.update()

    def update_possible_words_current_try(e):
        nonlocal tries
        dynamic_tries = tries.copy()
        dynamic_tries.append(try_input.value.upper())
        possible_categories = get_matching_categories(dynamic_tries)
        words_cat = get_words_from_categories(possible_categories, tries)
        possible_words = [w for w in words_cat if w.startswith(try_input.value.upper())]
        possible_words_label.value = "Possible words: " + (
            ", ".join(possible_words) if possible_words else "None"
        )
        page.update()

    def add_try(e):
        nonlocal current_prefix, tries

        if try_input.value:
            current_try = try_input.value.upper()
            tries.append(current_try)
            current_prefix = "".join(tries)

            try_input.value = ""
            entered_letters_label.value = "Entered tries: " + " ".join(tries)
            update_possible_words()

    def reset_game(e):
        nonlocal tries, current_prefix, possible_words
        tries = []
        current_prefix = ""
        possible_words = [word for words in word_codex.values() for word in words]

        entered_letters_label.value = "Entered tries: "
        possible_words_label.value = "Possible words: " + ", ".join(possible_words)
        try_input.value = ""
        page.update()

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
    translate_input = ft.TextField(
        hint_text="Enter text to translate", on_change=translate_to_wyler
    )
    translation_images = ft.GridView(
        expand=True,
        max_extent=60,
        spacing=5,
        run_spacing=5,
    )

    input_row = ft.Row([try_input, add_button], spacing=10)
    layout = ft.Column(
        [
            entered_letters_label,
            input_row,
            possible_words_label,
            reset_button,
            ft.Text(value="Wyler's Translator:"),
            translate_input,
            translation_images,
        ],
        spacing=20,
        expand=True,
    )

    page.title = "Shaolin hangman solver"
    page.add(layout)


ft.app(target=main)
