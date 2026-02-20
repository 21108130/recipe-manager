import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import quote

class RecipeScraper:
    """Recipe scraping utility"""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    @staticmethod
    def search_recipes(query):
        """Search recipes from multiple sources"""
        results = []
        print(f"Searching for: {query}")

        sources = [
            ('RecipeTin Eats', RecipeScraper.scrape_recipetineats),
            ('Simply Recipes', RecipeScraper.scrape_simplyrecipes),
            ('BBC Good Food', RecipeScraper.scrape_bbcgoodfood),
            ('Tasty', RecipeScraper.scrape_tasty),
            ('Allrecipes', RecipeScraper.scrape_allrecipes),
            ('Food Network', RecipeScraper.scrape_foodnetwork)
        ]

        for source_name, source_func in sources:
            try:
                print(f"Trying {source_name}...")
                recipes = source_func(query)
                if recipes:
                    print(f"✅ Found {len(recipes)} from {source_name}")
                    results.extend(recipes)
                else:
                    print(f"❌ No recipes from {source_name}")
            except Exception as e:
                print(f"⚠️ Error with {source_name}: {e}")
            time.sleep(1)

        print(f"📊 Total recipes found: {len(results)}")
        return results

    @staticmethod
    def scrape_recipetineats(query):
        """Scrape from RecipeTin Eats (very reliable)"""
        recipes = []
        try:
            url = f"https://www.recipetineats.com/?s={quote(query)}"
            response = requests.get(url, headers=RecipeScraper.HEADERS, timeout=10)

            if response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find recipe posts
            articles = soup.find_all('article', class_='post')[:5]

            for article in articles:
                try:
                    title_elem = article.find('h2', class_='entry-title')
                    link_elem = title_elem.find('a') if title_elem else None
                    img_elem = article.find('img', class_='wp-post-image')

                    if title_elem and link_elem:
                        recipe = {
                            'title': title_elem.text.strip(),
                            'url': link_elem['href'],
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'RecipeTin Eats',
                            'description': 'Trusted recipes from RecipeTin Eats'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"RecipeTin Eats error: {e}")

        return recipes

    @staticmethod
    def scrape_simplyrecipes(query):
        """Scrape from Simply Recipes"""
        recipes = []
        try:
            url = f"https://www.simplyrecipes.com/search?q={quote(query)}"
            response = requests.get(url, headers=RecipeScraper.HEADERS, timeout=10)

            if response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find recipe cards
            cards = soup.find_all('a', class_='card')[:5]

            for card in cards:
                try:
                    title_elem = card.find('h3', class_='card__title')
                    img_elem = card.find('img', class_='card__img')

                    if title_elem:
                        recipe = {
                            'title': title_elem.text.strip(),
                            'url': card['href'] if card.has_attr('href') else '#',
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'Simply Recipes',
                            'description': 'Classic and trusted recipes'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"Simply Recipes error: {e}")

        return recipes

    @staticmethod
    def scrape_bbcgoodfood(query):
        """Scrape from BBC Good Food"""
        recipes = []
        try:
            url = f"https://www.bbcgoodfood.com/search?q={quote(query)}"
            response = requests.get(url, headers=RecipeScraper.HEADERS, timeout=10)

            if response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('article', class_='card')[:5]

            for item in items:
                try:
                    title_elem = item.find('h2', class_='heading-4')
                    link_elem = item.find('a', href=True)
                    img_elem = item.find('img', class_='image')

                    if title_elem and link_elem:
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = 'https://www.bbcgoodfood.com' + link

                        recipe = {
                            'title': title_elem.text.strip(),
                            'url': link,
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'BBC Good Food',
                            'description': 'Recipes from BBC Good Food'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"BBC Good Food error: {e}")

        return recipes

    @staticmethod
    def scrape_tasty(query):
        """Scrape from Tasty"""
        recipes = []
        try:
            url = f"https://tasty.co/search?q={quote(query)}"
            response = requests.get(url, headers=RecipeScraper.HEADERS, timeout=10)

            if response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('div', class_='search-result')[:5]

            for item in items:
                try:
                    title_elem = item.find('span', class_='result-name')
                    link_elem = item.find('a', href=True)
                    img_elem = item.find('img', class_='photo')

                    if title_elem and link_elem:
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = 'https://tasty.co' + link

                        recipe = {
                            'title': title_elem.text.strip(),
                            'url': link,
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'Tasty',
                            'description': 'Viral recipes from Tasty'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"Tasty error: {e}")

        return recipes

    @staticmethod
    def scrape_allrecipes(query):
        """Scrape from Allrecipes with better headers"""
        recipes = []
        try:
            url = f"https://www.allrecipes.com/search?q={quote(query)}"

            # Use more browser-like headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try multiple selectors
            cards = soup.find_all(['div', 'article'], class_=re.compile(r'(card|recipe|search-result)', re.I))[:5]

            for card in cards:
                try:
                    title_elem = card.find(['h2', 'h3', 'h4'])
                    link_elem = card.find('a', href=True)
                    img_elem = card.find('img', src=True)

                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        link = link_elem['href']

                        if not link.startswith('http'):
                            link = 'https://www.allrecipes.com' + link

                        recipe = {
                            'title': title,
                            'url': link,
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'Allrecipes',
                            'description': 'Recipes from Allrecipes'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"Allrecipes error: {e}")

        return recipes

    @staticmethod
    def scrape_foodnetwork(query):
        """Scrape from Food Network"""
        recipes = []
        try:
            url = f"https://www.foodnetwork.com/search/{quote(query)}-"

            # Rotate user agents
            user_agents = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
            ]

            response = None
            for headers in user_agents:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        break
                except:
                    continue

            if not response or response.status_code != 200:
                return recipes

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try multiple selectors
            items = soup.find_all(['div', 'article'], class_=re.compile(r'(MediaBlock|card|result)', re.I))[:5]

            for item in items:
                try:
                    title_elem = item.find(['h2', 'h3', 'h4'])
                    link_elem = item.find('a', href=True)
                    img_elem = item.find('img', src=True)

                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        link = link_elem['href']

                        if not link.startswith('http'):
                            link = 'https://www.foodnetwork.com' + link

                        recipe = {
                            'title': title,
                            'url': link,
                            'image': img_elem.get('src') if img_elem else None,
                            'source': 'Food Network',
                            'description': 'Recipes from Food Network'
                        }
                        recipes.append(recipe)
                except:
                    continue

        except Exception as e:
            print(f"Food Network error: {e}")

        return recipes

    @staticmethod
    def get_recipe_details(url):
        """Get detailed recipe from a URL"""
        if not url:
            return None

        try:
            headers = RecipeScraper.HEADERS.copy()
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return RecipeScraper.get_fallback_recipe(url)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try schema.org first
            recipe = RecipeScraper.extract_schema_recipe(soup)

            if not recipe:
                recipe = RecipeScraper.extract_html_recipe(soup)

            if recipe:
                recipe['source_url'] = url
                return recipe

            return RecipeScraper.get_fallback_recipe(url)

        except Exception as e:
            print(f"Error fetching recipe details: {e}")
            return RecipeScraper.get_fallback_recipe(url)

    @staticmethod
    def extract_schema_recipe(soup):
        """Extract recipe from schema.org JSON-LD"""
        try:
            scripts = soup.find_all('script', type='application/ld+json')

            for script in scripts:
                try:
                    data = json.loads(script.string)

                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'Recipe' in str(item.get('@type', '')):
                                return RecipeScraper.parse_schema_item(item)
                    elif isinstance(data, dict):
                        if 'Recipe' in str(data.get('@type', '')):
                            return RecipeScraper.parse_schema_item(data)
                except:
                    continue
        except:
            pass
        return None

    @staticmethod
    def parse_schema_item(data):
        """Parse a single schema.org recipe item"""
        recipe = {
            'title': data.get('name', 'Recipe'),
            'description': data.get('description', ''),
            'ingredients': data.get('recipeIngredient', []),
            'instructions': [],
            'image': None
        }

        image = data.get('image')
        if isinstance(image, list):
            recipe['image'] = image[0] if image else None
        elif isinstance(image, dict):
            recipe['image'] = image.get('url')
        else:
            recipe['image'] = image

        instructions = data.get('recipeInstructions', [])
        for i, step in enumerate(instructions, 1):
            if isinstance(step, dict):
                text = step.get('text') or step.get('name') or ''
                if text:
                    recipe['instructions'].append(f"{i}. {text}")
            elif isinstance(step, str):
                recipe['instructions'].append(f"{i}. {step}")

        return recipe

    @staticmethod
    def extract_html_recipe(soup):
        """Extract recipe by parsing HTML"""
        recipe = {
            'title': 'Recipe',
            'description': '',
            'ingredients': [],
            'instructions': [],
            'image': None
        }

        h1 = soup.find('h1')
        if h1:
            recipe['title'] = h1.text.strip()

        ingredient_section = soup.find(['ul', 'div'], class_=re.compile(r'ingredient', re.I))
        if ingredient_section:
            for li in ingredient_section.find_all('li')[:10]:
                text = li.text.strip()
                if text and len(text) > 2:
                    recipe['ingredients'].append(text)

        instruction_section = soup.find(['ol', 'div'], class_=re.compile(r'instruction|step', re.I))
        if instruction_section:
            for i, step in enumerate(instruction_section.find_all('li')[:10], 1):
                text = step.text.strip()
                if text and len(text) > 10:
                    recipe['instructions'].append(f"{i}. {text}")

        img = soup.find('img', class_=re.compile(r'recipe|hero', re.I))
        if img:
            recipe['image'] = img.get('src') or img.get('data-src')

        return recipe

    @staticmethod
    def get_fallback_recipe(url):
        """Return fallback recipe"""
        domain = url.split('/')[2] if '://' in url else 'website'
        return {
            'title': f'Recipe from {domain}',
            'description': f'This recipe is from {domain}. Click the link below to view it.',
            'ingredients': ['📍 Please visit the original website for ingredients'],
            'instructions': ['📍 Please visit the original website for complete instructions'],
            'image': None
        }