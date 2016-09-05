import scrapy
from get_recipes.items import GetRecipesItem
import sys
sys.path.append('/home/pipersav/devarena/projects/cook-now')
from models import Recipe, Base
import pdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class RecipeSpider(scrapy.Spider):
    name = 'get_recipes'
    allowed_domains = ['paleoleap.com']
    #allowed_domain = ['allrecipes.com']
    #start_url = ['allrecipes.com']
    start_urls = ['http://paleoleap.com/paleo-diet-recipes/']
    recipe_links = []

    def parse(self, response):
        for link in response.xpath('//table[@class="listing-recipes"]/tbody/tr/td/a/@href').extract():
            #if link == 'http://paleoleap.com/greek-style-meatballs/':
            yield scrapy.Request(link, callback=self.parse_recipes)
            #else:
            #    print link

    def parse_recipes(self, response):
        link = response.url
        if link.endswith("/"):
            name = link.split("/")[-2]
        else:
            name = link.split("/")[-1]
            item['name'] = name
            item['link'] = str(link)
        ingredients = response.xpath('//ul/li[@itemprop="ingredients"]/text()').extract()
        instructions = response.xpath('//ol/li/text()').extract()
        ingredients = ','.join(ingredients)
        instructions = ','.join(instructions)
        print ingredients, instructions
        recipe = Recipe(name=name,
                        url_link=link,
                        ingredients=ingredients,
                        instructions=instructions)
        print "Adding recipe"
        session.add(recipe)
        session.commit()

