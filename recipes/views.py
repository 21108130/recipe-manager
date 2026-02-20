from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Recipe, Category, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, RecipeForm
from .utils.scraper import RecipeScraper

def home(request):
    """Home page with featured recipes"""
    recent_recipes = Recipe.objects.all()[:6]
    categories = Category.objects.all()
    context = {
        'recent_recipes': recent_recipes,
        'categories': categories
    }
    return render(request, 'recipes/home.html', context)

def recipe_list(request):
    """Show all recipes"""
    recipes = Recipe.objects.all()
    category = request.GET.get('category')
    if category:
        recipes = recipes.filter(category_id=category)
    context = {
        'recipes': recipes,
        'categories': Category.objects.all()
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, pk):
    """Show single recipe detail"""
    recipe = get_object_or_404(Recipe, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = recipe.likes.filter(id=request.user.id).exists()
    context = {
        'recipe': recipe,
        'is_liked': is_liked
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def recipe_create(request):
    """Create new recipe"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Create Recipe'})

@login_required
def recipe_update(request, pk):
    """Update recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Update Recipe'})

@login_required
def recipe_delete(request, pk):
    """Delete recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted!')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def like_recipe(request, pk):
    """Like/unlike recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        messages.info(request, 'Recipe unliked')
    else:
        recipe.likes.add(request.user)
        messages.success(request, 'Recipe liked!')
    return redirect('recipe_detail', pk=recipe.pk)

@login_required
def profile(request):
    """User profile page"""
    user_recipes = Recipe.objects.filter(created_by=request.user)
    liked_recipes = request.user.liked_recipes.all()
    context = {
        'user_recipes': user_recipes,
        'liked_recipes': liked_recipes
    }
    return render(request, 'registration/profile.html', context)

@login_required
def profile_update(request):
    """Update user profile"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile_update.html', context)

def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for user
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome {user.username}!')
            return redirect('recipe_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})

def search_recipes(request):
    """Search recipes from web and local database"""
    query = request.GET.get('q', '').strip()
    web_recipes = []
    local_recipes = []

    if query:
        
        local_recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        ).distinct()

        
        try:
            scraper = RecipeScraper()
            web_recipes = scraper.search_recipes(query)

            # Debug information
            print(f"Search query: '{query}'")
            print(f"Local recipes found: {len(local_recipes)}")
            print(f"Web recipes found: {len(web_recipes)}")

        except AttributeError as e:
            print(f"AttributeError in web search: {e}")
            # Try alternative methods
            try:
                scraper = RecipeScraper()
                web_recipes = []

                # Try each method individually if they exist
                if hasattr(scraper, 'scrape_bbcgoodfood'):
                    bbc_recipes = scraper.scrape_bbcgoodfood(query)
                    web_recipes.extend(bbc_recipes)
                    print(f"BBC Good Food: {len(bbc_recipes)} recipes")

                if hasattr(scraper, 'scrape_tasty'):
                    tasty_recipes = scraper.scrape_tasty(query)
                    web_recipes.extend(tasty_recipes)
                    print(f"Tasty: {len(tasty_recipes)} recipes")

            except Exception as alt_error:
                print(f"Alternative search error: {alt_error}")
                web_recipes = []

        except Exception as e:
            print(f"Web search error: {e}")
            web_recipes = []

    context = {
        'local_recipes': local_recipes,
        'web_recipes': web_recipes,
        'query': query,
        'total_local': len(local_recipes),
        'total_web': len(web_recipes),
        'has_results': len(local_recipes) > 0 or len(web_recipes) > 0
    }
    return render(request, 'recipes/search_results.html', context)

def recipe_detail_external(request):
    """Show recipe from external URL"""
    url = request.GET.get('url')
    if not url:
        messages.error(request, 'No URL provided')
        return redirect('search')

    # Clean URL
    url = url.replace('//www.foodnetwork.com//', '//www.foodnetwork.com/')
    url = url.replace('//www.allrecipes.com//', '//www.allrecipes.com/')

    try:
        scraper = RecipeScraper()
        recipe = scraper.get_recipe_details(url)

        if not recipe:
            # Fallback recipe
            domain = url.split('/')[2] if '://' in url else 'website'
            recipe = {
                'title': f'Recipe from {domain}',
                'description': 'This recipe is from an external website. Click the button below to view the original recipe.',
                'ingredients': ['📍 Please visit the original website for complete ingredients list'],
                'instructions': ['📍 Please visit the original website for step-by-step instructions'],
                'image': None,
                'prep_time': '',
                'cook_time': '',
                'total_time': '',
                'yield': ''
            }

        context = {
            'recipe': recipe,
            'source_url': url
        }
        return render(request, 'recipes/external_recipe.html', context)

    except Exception as e:
        print(f"Error in recipe_detail_external: {e}")
        # Fallback recipe
        domain = url.split('/')[2] if '://' in url else 'website'
        context = {
            'recipe': {
                'title': f'Recipe from {domain}',
                'description': 'Click the button below to view the original recipe on the source website.',
                'ingredients': ['📍 Visit original website for ingredients'],
                'instructions': ['📍 Visit original website for instructions'],
                'image': None,
                'prep_time': '',
                'cook_time': '',
                'total_time': '',
                'yield': ''
            },
            'source_url': url
        }
        return render(request, 'recipes/external_recipe.html', context)

# ===== UPDATED CATEGORY RECIPES FUNCTION =====
def category_recipes(request, category_id):
    """Show recipes by category - both local and web"""
    category = get_object_or_404(Category, pk=category_id)


    local_recipes = Recipe.objects.filter(category=category)

    
    web_recipes = []
    try:
        scraper = RecipeScraper()
        
        web_recipes = scraper.search_recipes(category.name)
        print(f"Found {len(web_recipes)} web recipes for category '{category.name}'")

        
        seen_urls = set()
        unique_recipes = []
        for recipe in web_recipes:
            if recipe['url'] not in seen_urls:
                seen_urls.add(recipe['url'])
                unique_recipes.append(recipe)

        web_recipes = unique_recipes[:8]  # Max 8 web recipes

    except Exception as e:
        print(f"Error fetching web recipes for category: {e}")
        web_recipes = []

    context = {
        'category': category,
        'local_recipes': local_recipes,
        'web_recipes': web_recipes,
        'total_local': len(local_recipes),
        'total_web': len(web_recipes),
        'has_recipes': len(local_recipes) > 0 or len(web_recipes) > 0
    }
    return render(request, 'recipes/category_recipes.html', context)

@login_required
def saved_recipes(request):
    """Show user's saved/liked recipes"""
    saved_recipes = request.user.liked_recipes.all()
    context = {
        'saved_recipes': saved_recipes
    }
    return render(request, 'recipes/saved_recipes.html', context)

def about(request):
    """About page"""
    return render(request, 'recipes/about.html', {})

def contact(request):
    """Contact page"""
    return render(request, 'recipes/contact.html', {})

def terms(request):
    """Terms and conditions page"""
    return render(request, 'recipes/terms.html', {})

def privacy(request):
    """Privacy policy page"""
    return render(request, 'recipes/privacy.html', {})

# Error handlers
def handler404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)

def handler403(request, exception):
    """Custom 403 error page"""
    return render(request, 'errors/403.html', status=403)

def handler400(request, exception):
    """Custom 400 error page"""
    return render(request, 'errors/400.html', status=400)
