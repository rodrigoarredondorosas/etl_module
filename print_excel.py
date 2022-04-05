from config import (
    RELATION,
    MOCKUP_CLIENT,
    RELATION_FIELDS,
)

from utils import print_excel


def create_excel(client, relations, relations_fields):
    print_excel(client, relations, relations_fields)


if __name__ == "__main__":
    create_excel(MOCKUP_CLIENT, RELATION, RELATION_FIELDS)
