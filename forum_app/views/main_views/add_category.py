import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from slugify import slugify

from forum_app.models import Category


# from forum_app.forms import AddCategoryForm


# class CreateCategory(LoginRequiredMixin, CreateView):
#     model = Category
#     form_class = AddCategoryForm
#     template_name = 'forum_app/add_category.html'


def ajax_create_category(request):
    if request.method == 'POST':

        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            cat_name = data.get('name')
            cat_slug = slugify(cat_name)

            exist_cat = Category.objects.filter(slug=cat_slug)

            if not exist_cat:
                new_cat = Category(name=cat_name, slug=cat_slug, user=request.user)

                new_cat.save()
            else:
                new_cat = exist_cat.first()

            response_data = {
                'id': new_cat.id,
                'name': new_cat.name,
            }

            return JsonResponse(response_data)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Object not found'}, status=404)

    # В случае GET-запроса верните HTTP 405 Method Not Allowed
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def ajax_del_category(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        cat_list = [int(id_cat) for id_cat in data.get('cat_list', [])]
        empty_cat = Category.objects.filter(id__in=cat_list, post__isnull=True).distinct()

        deleted_cats = []
        for cat in empty_cat:
            deleted_cats.append(f"{cat.id}")
            cat.delete()

        return JsonResponse({'cat_list': deleted_cats})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
