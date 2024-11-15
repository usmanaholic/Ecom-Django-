from .models import Category

def categories_context(request):
    categories = Category.objects.prefetch_related('sub_category').all()
    return {'categories': categories}