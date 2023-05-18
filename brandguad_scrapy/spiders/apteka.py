import time

import scrapy
from html2text import html2text


class AptekaSpider(scrapy.Spider):
    name = "apteka"
    allowed_domains = ["apteka-ot-sklada.ru"]

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = categories.split(",")

    def start_requests(self):
        limit = 30 # Кол-во объекто, котоыре необходимо спарсить
        city = 92 # ID города для передачи в cookies
        cookies = {"city": city}
        corrected_categories = [
            category.replace("/", "%2F") for category in self.categories
        ]
        urls = [
            f"https://apteka-ot-sklada.ru/api/catalog"
            f"/search?sort=popindex&slug={category}&limit={limit}"
            for category in corrected_categories
        ]

        for url in urls:
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        data = response.json()["goods"]
        ids = (str(good["id"]) for good in data)
        links = (f"https://apteka-ot-sklada.ru/api/catalog/{id}" for id in ids)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        timestamp = time.time()
        # Условные конструкции вынесены в начало для удобства
        if response.json()["oldCost"] is not None:
            sale_percent = round(
                (response.json()["oldCost"] - response.json()["cost"])
                / response.json()["oldCost"]
                * 100
            )
            sale_tag = f"Скидка {sale_percent}%"
        else:
            sale_tag = None
        if len(response.json()["stickers"]) < 1:
            marketing_tags = None
        else:
            marketing_tags = [
                tag["name"] for tag in response.json()["stickers"]
            ]
        section = [
            parent["name"] for parent in response.json()["category"]["parents"]
        ] + [response.json()["category"]["name"]]
        if len(response.json()["images"]) > 1:
            set_images = [
                f'https://apteka-ot-sklada.ru/{response.json()["images"][i]}'
                for i in range(1, len(response.json()["images"]))
            ]
        else:
            set_images = []
        description = (
            None
            if response.json()["description"] is None
            else html2text(response.json()["description"])
        )
        yield {
            "timestamp": timestamp,
            "RPC": response.json()["id"],
            "url": f"https://apteka-ot-sklada.ru/"
                   f"catalog/{response.json()['slug']}",
            "title": response.json()["name"],
            "marketing_tags": marketing_tags,
            "brand": response.json()["producer"],
            "section": section,
            "price_data": {
                "current": response.json()["cost"],
                "original": response.json()["oldCost"],
                "sale_tag": sale_tag,
            },
            "stock": {
                "in_stock": response.json()["inStock"],
                "count": response.json()["availability"],
            },
            "assets": {
                "main_image": f"https://apteka-ot-sklada.ru"
                              f"{response.json()['images'][0]}",
                "set_images": set_images,
            },
            "metadata": {
                "description": description,
                "country": response.json()["country"],
                "delivery": response.json()["delivery"],
            },
        }
