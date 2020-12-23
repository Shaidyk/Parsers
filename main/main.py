from parsers.parser_work import WorkContent
from parsers.parser_rabota import RabotaContent
from db import DbCreator


if __name__ == '__main__':
    content = RabotaContent().get_info()
    db = DbCreator('rabota')
    db.set_table(content)

    content = WorkContent().get_info()
    db = DbCreator('work')
    db.set_table(content)
