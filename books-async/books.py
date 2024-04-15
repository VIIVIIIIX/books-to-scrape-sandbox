import aiohttp
import asyncio
from bs4 import BeautifulSoup
from dataclasses import dataclass
import csv


@dataclass
class Books:
    upc_id: str
    title: str
    price: str
    tag: str
    in_stock: str
    review: str


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all_pages(session, urls)
        return data


async def get_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_all_pages(session, urls):
    tasks = list()
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


def get_book_links(results):
    book_urls = list()
    for html in results:
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("h3"):
            book_urls.append(
                "https://books.toscrape.com/catalogue/" + item.find("a").get("href")
            )
    return book_urls


def parse_book_links(results):
    for html in results:
        soup = BeautifulSoup(html, "html.parser")

        upc_id = soup.find_all("td")[0].text  # type: ignore
        title = soup.find("div", class_="col-sm-6 product_main").h1.text  # type: ignore
        price = soup.find("div", class_="col-sm-6 product_main").find_all("p")[0].text  # type: ignore
        tag = soup.find("ul", class_="breadcrumb").find_all("li")[2].a.text  # type: ignore
        in_stock = (
            soup.find("div", class_="col-sm-6 product_main")
            .find_all("p")[1]  # type: ignore
            .get_text()
            .strip()
            .split(" ")[2]
            .replace("(", "")
        )
        review = (
            soup.find("div", class_="col-sm-6 product_main")
            .find_all("p")[2]  # type: ignore
            .get("class")[1]
            .lower()
        )

        yield Books(
            upc_id=upc_id,
            title=title,
            price=price,
            tag=tag,
            in_stock=in_stock,
            review=review,
        )


if __name__ == "__main__":
    urls = [f"https://books.toscrape.com/catalogue/page-{n}.html" for n in range(1, 51)]
    results = asyncio.run(main(urls))
    urls = get_book_links(results)
    results = asyncio.run(main(urls))

    with open("./books.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["upc_id", "title", "price", "tag", "in_stock", "review"])

        for data in parse_book_links(results):
            writer.writerow(
                [
                    data.upc_id,
                    data.title,
                    data.price,
                    data.tag,
                    data.in_stock,
                    data.review,
                ]
            )

            print(data)
            print()

    print("Books scraped successfully!")
