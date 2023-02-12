from db import db

book_data = [
    {
        "title": 'The Way of Kings',
        "author": 'Brandon Sanderson',
        "rating": 9,
        "pages": 400,
        "genres": ['fantasy'],
        "reviews": [
            {"name": 'Yoshi', "body": 'Great books!!'},
            {"name": 'Mario', "body": 'So so'}
        ]
    },
    {
        "title": 'The Light Fantastic',
        "author": 'Terry Pratchet',
        "pages": 250,
        "rating": 6,
        "genres": ['fantasy', 'magic'],
        "reviews": [
            {"name": 'Luigi', "body": 'It was pretty good'},
            {"name": 'Bowser', "body": 'Loved It!!!'}
        ]
    },
    {
        "title": 'The Name of the Wind',
        "author": 'Patrick Rothfuss',
        "pages": 500,
        "rating": 10,
        "genres": ['fantasy'],
        "reviews": [{"name": 'Peach', "body": 'One of my favs'}]
    },
    {
        "title": 'The Color of Magic',
        "author": 'Terry Pratchet',
        "pages": 360,
        "rating": 8,
        "genres": ['fantasy', 'magic'],
        "reviews": [
            {"name": 'Luigi', "body": 'It was OK'},
            {"name": 'Bowser', "body": 'Really good book'}
        ]
    },
    {
        "title": '1984',
        "author": 'George Orwell',
        "pages": 300,
        "rating": 6,
        "genres": ['dystopian', 'sci-fi', 'fantasy', '1', '2'],
        "reviews": [
            {"name": 'Peach', "body": 'Not my cup of tea'},
            {"name": 'Mario', "body": 'Meh'}
        ]
    },
    {
        "title": 'The Final Empire',
        "author": 'Brandon Sanderson',
        "rating": 9,
        "pages": 420,
        "genres": ['fantasy', 'magic'],
        "reviews": [
            {"name": 'Shaun', "body": "Couldn't put this book down"},
            {"name": 'Chun-Li', "body": 'Love it'}
        ]
    }
]

db.drop_collection("books")
books = db.get_collection("books")
books.insert_many(book_data)
