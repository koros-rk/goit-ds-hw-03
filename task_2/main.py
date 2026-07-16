import asyncio

from entities.author import Author
from entities.post import Post
from repositories.authors import AuthorsRepository
from repositories.posts import PostsRepository
from utils import fetch_posts, fetch_author, has_next_page, logger, dump_to_json


async def main():
    page = 1

    posts: list[Post] = []
    authors: list[Author] = []

    while True:
        scrapped_posts, html = await fetch_posts(page)

        authors_links = {
            post.author_link
            for post in scrapped_posts
            if post.author_name not in map(str, authors)
        }

        tasks = [fetch_author(link) for link in authors_links]
        authors += filter(None, await asyncio.gather(*tasks))
        posts += scrapped_posts

        if not has_next_page(html):
            break
        page += 1

    try:
        with PostsRepository() as posts_repository:
            posts_repository.cleanse()
            posts_repository.save_many(posts)
            logger.info(f"Saved {len(posts)} posts")
    except Exception as e:
        logger.error(f"Unable to save posts: {e}")
        return

    try:
        with AuthorsRepository() as authors_repository:
            authors_repository.cleanse()
            authors_repository.save_many(authors)
            logger.info(f"Saved {len(authors)} authors")
    except Exception as e:
        logger.error(f"Unable to save authors: {e}")
        return

    dump_to_json([p.serialize() for p in posts], "../dump/posts.json")
    dump_to_json([a.serialize() for a in authors], "../dump/authors.json")


if __name__ == "__main__":
    asyncio.run(main())
