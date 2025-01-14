import common
from src.table_and_fig_ref_extraction.ExtractTableAndFigRefPatterns import *


def read_claims(read_file):
    with open(read_file, 'r') as f:
        text = f.read()
        return text


def find_tables_ref(text):
    """
    Given the claim text, this method will find the number of tables mentioned in the text and return
    """
    table_numbers = []
    additional_table_numbers_with_alpha_chars = []

    table_refs, tables_with_roman_numbers = findTableRefs(text)

    # Convert the roman numbers to integers
    for table_ref in tables_with_roman_numbers:
        roman_number = table_ref.split(" ")[1]
        roman = {'I': 1, 'V': 5, 'X': 10, 'IV': 4, 'IX': 9, 'XL': 40, 'L': 50, 'XC': 90, 'C': 100, 'CD': 400, 'D': 500,
                 'CM': 900, 'M': 1000}
        i = 0
        num = 0
        while i < len(roman_number):
            if i + 1 < len(roman_number) and roman_number[i:i + 2] in roman:
                num += roman[roman_number[i:i + 2]]
                i += 2
            else:
                num += roman[roman_number[i]]
                i += 1
        table_numbers.append(str(num))

    for table_ref in table_refs:
        if '\xa0' in table_ref:
            table = table_ref.split("\xa0")
        else:
            table = table_ref.split(" ")
        if table[0].lower() == "table":
            contains_alpha_char = False
            for character in table[1]:
                if character.isalpha():
                    contains_alpha_char = True
            if contains_alpha_char:
                additional_table_numbers_with_alpha_chars.append(table[1])
            else:
                table_numbers.append(table[1])
        elif table[0].lower() == "tables":
            # check for 'and'
            if "and" in table:
                contains_alpha_char = False
                for table_num in [table[1], table[3]]:
                    for character in table_num:
                        if character.isalpha():
                            contains_alpha_char = True
                    if contains_alpha_char:
                        additional_table_numbers_with_alpha_chars.append(table_num)
                    else:
                        table_numbers.append(table_num)
            # check for the long dash
            elif "–" in table[1]:
                table_numbers.extend(table[1].split("–"))
            # check for the small dash
            elif "-" in table[1]:
                table_numbers.extend(table[1].split("-"))

    return table_numbers, additional_table_numbers_with_alpha_chars


def find_figures_ref(text):
    """
    Given the text extracted from the paper, this method will find the number of figures in the text and return
    """

    figure_numbers = []
    additional_figures_numbers_with_alpha_chars = []

    figure_refs, figs_with_roman_numbers = findFigRefs(text)

    # Convert the roman numbers to integers
    for fig_ref in figs_with_roman_numbers:
        roman_number = fig_ref.split(" ")[1]
        roman = {'I': 1, 'V': 5, 'X': 10, 'IV': 4, 'IX': 9, 'XL': 40, 'L': 50, 'XC': 90, 'C': 100, 'CD': 400, 'D': 500,
                 'CM': 900, 'M': 1000}

        i = 0
        num = 0
        while i < len(roman_number):
            if i + 1 < len(roman_number) and roman_number[i:i + 2] in roman:
                num += roman[roman_number[i:i + 2]]
                i += 2
            else:
                num += roman[roman_number[i]]
                i += 1

        figure_numbers.append(str(num))

    for figure_ref in figure_refs:
        if 'figs' in figure_ref.lower() or 'figures' in figure_ref.lower():
            if '\xa0' in figure_ref:
                figure = figure_ref.split("\xa0")
            else:
                figure = figure_ref.split(" ")
            # check for 'and'
            if "and" in figure:
                contains_alpha_char = False
                for fig_num in [figure[1], figure[3]]:
                    for character in fig_num:
                        if character.isalpha():
                            contains_alpha_char = True
                    if contains_alpha_char:
                        additional_figures_numbers_with_alpha_chars.append(fig_num)
                    else:
                        figure_numbers.append(fig_num)
            # check for the long dash
            elif "–" in figure[1]:
                figure_numbers.extend(figure[1].split("–"))
            # check for the small dash
            elif "-" in figure[1]:
                figure_numbers.extend(figure[1].split("-"))
        else:
            if '\xa0' in figure_ref:
                figure = figure_ref.split("\xa0")
            else:
                figure = figure_ref.split(" ")
            contains_alpha_char = False
            for character in figure[1]:
                if character.isalpha():
                    contains_alpha_char = True
            if contains_alpha_char:
                additional_figures_numbers_with_alpha_chars.append(figure[1])
            else:
                figure_numbers.append(figure[1])

    return figure_numbers, additional_figures_numbers_with_alpha_chars


def get_total_mentions_of_display_items_from_claim_text(display_item_numbers, additional_display_items_with_alpha_chars):

    if len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) == 0:
        return 0
    elif len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(additional_display_items_with_alpha_chars)
    elif len(display_item_numbers) != 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(display_item_numbers) + len(additional_display_items_with_alpha_chars)
    else:
        return len(display_item_numbers)


def get_unique_mentions_of_display_items_from_claim_text(display_item_numbers,
                                                        additional_display_items_with_alpha_chars):
    if len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) == 0:
        return 0
    elif len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(set(additional_display_items_with_alpha_chars))
    elif len(display_item_numbers) != 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(set(display_item_numbers)) + len(set(additional_display_items_with_alpha_chars))
    else:
        return len(set(display_item_numbers))


def get_display_items_from_claim(filename):
    text = read_claims(filename)
    table_numbers, additional_table_numbers_with_alpha_chars = find_tables_ref(text)
    figure_numbers, additional_figures_numbers_with_alpha_chars = find_figures_ref(text)

    total_mentions_of_table_ref_in_the_claim = \
        get_total_mentions_of_display_items_from_claim_text(table_numbers, additional_table_numbers_with_alpha_chars)
    total_mentions_of_figure_ref_in_the_claim = \
        get_total_mentions_of_display_items_from_claim_text(figure_numbers, additional_figures_numbers_with_alpha_chars)

    unique_mentions_of_table_ref_in_the_claim = \
        get_unique_mentions_of_display_items_from_claim_text(table_numbers, additional_table_numbers_with_alpha_chars)
    unique_mentions_of_figure_ref_in_the_claim = \
        get_unique_mentions_of_display_items_from_claim_text(figure_numbers, additional_figures_numbers_with_alpha_chars)

    return (total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim,
            unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim)


if __name__ == "__main__":
    # input the claim in a text file
    input_file = "./input/claims/FromGROBID/Fujiwara_Econometrica_2015_BbLg.txt"
    output_file = "./output/claim_level/output.json"
    total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim, \
    unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim = \
        get_display_items_from_claim(input_file)

    total_mentions_of_tables_and_figures_json = \
        common.create_json(total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim)
    unique_mentions_of_tables_and_figures_json = \
        common.create_json(unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim)
    json_output = common.create_claim_output_json(total_mentions_of_tables_and_figures_json,
                                                  unique_mentions_of_tables_and_figures_json)
    common.write_to_json(json_output, output_file)
