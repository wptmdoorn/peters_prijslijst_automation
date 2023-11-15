from parse_site import get_product_information
from write_docx import write_peters_docx

URL = "https://petersaanhangwagens.nl/product/hapert-azure-h-1-1350-verlaagd-260x150-2/"

if __name__ == "__main__":
    info = get_product_information(URL)
    write_peters_docx(info)

    print(info)
