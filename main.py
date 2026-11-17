from lab_parser_unittest.src.parser import ForumParser


url = "https://quotes.toscrape.com/"

parser = ForumParser()

data = parser.parse_page(url)

print("Найдено записей:", len(data))

for item in data:
    print("ID:", item["id"])
    print("Автор:", item["name"])
    print("Текст:", item["message"])
    print()