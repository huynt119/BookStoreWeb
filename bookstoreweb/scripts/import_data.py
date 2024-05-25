import csv
from webapp.models import *
            
def run():
    Book.objects.all().delete()
    UserAccount.objects.all().delete()
    Rating.objects.all().delete()
    Tag.objects.all().delete()

    with open("./data/tags.csv", 'r', encoding= "utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Tag.objects.create(
                tag = row['tag'],
                tag_id = row['id']
            )

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
                price=row['price'],
            )
        

    with open("./data/account.csv", 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            UserAccount.objects.create_user(
                id = row['id'],
                username = row['username'],
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
                user = UserAccount.objects.get(id = row['user_id']),
                rating = row['rating']
            )

    with open("./data/tag_id.csv", 'r', encoding= "utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book.objects.get(item_id = row['item_id'])
            tag = Tag.objects.get(tag_id = row['tag_id'])
            book.book_tags.add(tag)
            
        
            