import csv
from webapp.models import Book, Rating, User, Tag, BookTag
            
def run():
    Book.objects.all().delete()
    User.objects.all().delete()
    Rating.objects.all().delete()
    Tag.objects.all().delete()
    BookTag.objects.all().delete()

    with open("./data/booksdata.csv", 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Book.objects.create(
                item_id = row['item_id'],
                url = row['url'],
                title=row['title'],
                authors=row['authors'],
                lang = row['lang'],
                img = row['img'],
                year = row['year'],
                description = row['description'],
                price=row['price']
            )

    with open("./data/usersdata.csv", 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            User.objects.create(
                user_id = row['id'],
                first_name = row['first_name'],
                last_name = row['last_name'],   
                email = row['email'],
                password = row['password'],
                phone_num = row['phone_num'],
                address = row['address'],
            )

    with open("./data/ratings.csv", 'r', encoding= "utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Rating.objects.create(
                item = Book.objects.get(item_id = row['item_id']),
                user = User.objects.get(user_id = row['user_id']),
                rating = row['rating']
            )

    with open("./data/tags.csv", 'r', encoding= "utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Tag.objects.create(
                tag = row['tag'],
                tag_id = row['id']
            )

    with open("./data/tag_id.csv", 'r', encoding= "utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            BookTag.objects.create(
                item_tag = Book.objects.get(item_id = row['item_id']),
                id_tag = Tag.objects.get(tag_id = row['tag_id']),
            )
            