
import os
import sys
sys.path.append(os.getcwd())

# test a parser


def parse():
    from app.templates.peters_heesch.parser import get_product_information
    url = "https://petersaanhangwagens.nl/product/anssems-bakwagen-gt-750-r-251x126/"

    print(get_product_information(url))


print(sys.path)
parse()
