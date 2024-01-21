
import os
import sys
sys.path.append(os.getcwd())

# test a parser


def parse():
    from app.templates.peters_heesch.parser import get_product_information
    url = "https://petersaanhangwagens.nl/product/hapert-cobalt-hm-2-ferro-3500-paraboolvering-verlaagd-375x180-2/"

    print(get_product_information(url))


print(sys.path)
parse()
