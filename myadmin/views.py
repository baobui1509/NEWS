from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from myadmin.models import Category, Article, Contact, Tag
from .forms import *
from django.utils.text import slugify
from bs4 import BeautifulSoup
from .define import *
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
import os



def home_index(request):
    return render(request, 'myadmin/pages/home/index.html')


# def category_index(request):
#     items = Category.objects.all()
#     paginator = Paginator(items, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     all_count = items.count()
#     published_count = Category.objects.filter(status='published').count()
#     pending_count = Category.objects.filter(status='pending').count()
#     draft_count = Category.objects.filter(status='draft').count()
#     return render(request, 'myadmin/pages/category/index.html', {
#         'items': items,
#         'page_obj': page_obj,
#         'all_count': all_count,
#         'published_count': published_count,
#         'pending_count': pending_count,
#         'draft_count': draft_count
#     })

def category_index(request):
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', 'all')

    items = Category.objects.all()

    if search != 'all':
        items = items.filter(name__icontains=search)

    all_count = items.count()
    published_count = items.filter(status='published').count()
    pending_count = items.filter(status='pending').count()
    draft_count = items.filter(status='draft').count()

    if status != 'all':
        items = items.filter(status=status)

    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    list_status_count = {
        "all": {"count": all_count, "name": "All"},
        "published": {"count": published_count, "name": dict(CATEGORY_STATUS_CHOICES)['published']},
        "pending": {"count": pending_count, "name": dict(CATEGORY_STATUS_CHOICES)['pending']},
        "draft": {"count": draft_count, "name": dict(CATEGORY_STATUS_CHOICES)['draft']}
    }

    return render(request, 'myadmin/pages/category/index.html', {
        'items': items,
        'page_obj': page_obj,
        'status': status,
        'list_status_count': list_status_count,
    })


def generate_unique_slug(base_slug):
    slug = base_slug
    counter = 1
    while Category.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def category_create(request):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_message'] = 'Thêm danh mục thành công!'
            if request.POST.get('action') == 'submit':
                pass
            elif request.POST.get('action') == 'apply':
                slug = request.POST.get('slug')
                return redirect(reverse('category_edit', args=[slug]))
            else:
                return redirect(reverse('category_index', args=[]))
        else:
            FLAG_ERROR = True
            for field, errors in form.errors.items():
                for error in errors:
                    if (field == 'slug' and 'Slug này đã tồn tại' in error):
                        FLAG_ERROR = False
            if (FLAG_ERROR):
                request.session['error_message'] = form.errors
            else:
                # soup = BeautifulSoup(form.as_p(), 'html.parser')
                # slug_input = soup.find('input', {'name': 'slug'})
                # slug_value = slug_input['value'] if slug_input else None
                # new_form = CategoryForm(initial={**cleaned_data, 'slug': generate_unique_slug(slug_value)})
                # form = CategoryForm(initial={'slug': generate_unique_slug(slug_value)})
                post_data = request.POST.copy()
                post_data['slug'] = generate_unique_slug(post_data['slug'])
                new_form = CategoryForm(post_data)
                new_form.save()
                request.session['success_message'] = 'Thêm danh mục thành công!'
                if request.POST.get('action') == 'submit':
                    pass
                elif request.POST.get('action') == 'apply':
                    slug = request.POST.get('slug')
                    return redirect(reverse('category_edit', args=[slug]))
                else:
                    return redirect(reverse('category_index', args=[]))
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/category/create.html', {
        'success_message': success_message,
        'error_message': error_message,
        'category_status_choices': CATEGORY_STATUS_CHOICES,
        'category_layout_choices': CATEGORY_LAYOUT_CHOICES,
    })


def category_edit(request, id):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    item = get_object_or_404(Category, id=id)
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # item.name = request.POST.get('name')
            # item.slug = request.POST.get('slug')
            # item.is_homepage = request.POST.get('is_homepage') == 'on'
            # item.layout = request.POST.get('layout')
            # item.status = request.POST.get('status')
            for key, value in request.POST.items():
                if hasattr(item, key):
                    setattr(item, key, value)

            setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
            item.save()
            request.session['success_message'] = 'Chỉnh sửa thành công!'
            if request.POST.get('action') == 'apply':
                request.session['FLAG_MESSAGE'] = True
                # return redirect(reverse('category_edit', args=[item.id]))
            else:
                return redirect(reverse('category_index', args=[]))
        else:
            existSlug = True
            for field, errors in form.errors.items():
                for error in errors:
                    print('error:', error)
                    if not (field == 'slug' and 'Slug này đã tồn tại' in error):
                        request.session['error_message'] = form.errors
                        existSlug = False
            if (existSlug):
                # item.is_homepage = request.POST.get('is_homepage') == 'on'
                # item.layout = request.POST.get('layout')
                # item.status = request.POST.get('status')
                old_slug = item.slug
                for key, value in request.POST.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
                if (old_slug != item.slug):
                    item.slug = generate_unique_slug(item.slug)
                item.save()
                if request.POST.get('action') == 'apply':
                    request.session['FLAG_MESSAGE'] = True
                    request.session['success_message'] = 'Chỉnh sửa thành công!'

                    # return redirect(reverse('category_edit', args=[item.id]))
                else:
                    return redirect(reverse('category_index', args=[]))
            else:
                request.session['FLAG_MESSAGE'] = True
                request.session['error_message'] = form.errors
    success_message = ''
    error_message = ''
    FLAG_MESSAGE = request.session.pop('FLAG_MESSAGE', False)
    if (FLAG_MESSAGE):
        success_message = request.session.pop('success_message', None)
        error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/category/edit.html', {
        'item': item,
        'success_message': success_message,
        'error_message': error_message,
        'category_status_choices': CATEGORY_STATUS_CHOICES,
        'category_layout_choices': CATEGORY_LAYOUT_CHOICES,

    })

def category_delete_checker(item, type):
    if type == 'category':
        category_id = item.id
        Article.objects.filter(category__id=category_id).delete()

def item_delete(request, item_type, id):
    model_mapping = {
            'category': Category,
            'article': Article,
            'contact': Contact,
            'tag': Tag
        }
    model = model_mapping.get(item_type, None)

    item = get_object_or_404(model, id=id)

    if request.method == 'POST':
        # category_delete_checker(item, item_type)
        try:
            try:
                if item.image:
                    old_image_path = item.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
                        print(f'Đã xoá {old_image_path}')
            except AttributeError:
                pass
            item.delete()
            return JsonResponse({'success': True, 'message': 'Đã xóa thành công.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Có lỗi xảy ra khi xóa.'})
    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ.'})


def bulk_delete(request, item_type):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_ids = data.get('item_ids', [])
        model_mapping = {
            'category': Category,
            'article': Article,
            'contact': Contact,
            'tag': Tag
        }
        model = model_mapping.get(item_type, None)

        # model = Category if item_type == 'category' else Article if item_type == 'article' else None
        items = model.objects.filter(id__in=[int(item) for item in item_ids])
        for item in items:
            try:
                if item.image:
                    old_image_path = item.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
                        print(f'Đã xoá {old_image_path}')
            except AttributeError:
                pass
            # category_delete_checker(item, item_type)
            item.delete()
        # model.objects.filter(id__in=[int(item) for item in item_ids]).delete()
        return JsonResponse({'success': True, 'message': 'Đã xóa thành công.'})
    return JsonResponse({'success': False, 'message': 'Có lỗi xảy ra khi xóa.'})


def article_index(request):
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', 'all')

    items = Article.objects.all()

    if search != 'all':
        items = items.filter(name__icontains=search)

    all_count = items.count()
    published_count = items.filter(status='published').count()
    pending_count = items.filter(status='pending').count()
    draft_count = items.filter(status='draft').count()

    if status != 'all':
        items = items.filter(status=status)

    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    list_status_count = {
        "all": {"count": all_count, "name": "All"},
        "published": {"count": published_count, "name": dict(CATEGORY_STATUS_CHOICES)['published']},
        "pending": {"count": pending_count, "name": dict(CATEGORY_STATUS_CHOICES)['pending']},
        "draft": {"count": draft_count, "name": dict(CATEGORY_STATUS_CHOICES)['draft']}
    }
    return render(request, 'myadmin/pages/article/index.html', {
        'items': items,
        'page_obj': page_obj,
        'status': status,
        'list_status_count': list_status_count,
    })

def update_tags_create(request, article):
    tag_names = json.loads(request.POST.get('tags', ''))
    tags_list = [tag['value'].strip() for tag in tag_names if 'value' in tag and tag['value'].strip()]    
    for tag_name in tags_list:
        tag_name = tag_name.strip()
        if tag_name:
            tag_slug = slugify(tag_name)
            tag, created = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
            article.tags.add(tag)

def article_create(request):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    form = ArticleForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            # print('is_homepage: ', form.cleaned_data['is_homepage'])
            request.session['success_message'] = 'Thêm danh mục thành công!'
            if request.POST.get('action') == 'submit':
                pass
            elif request.POST.get('action') == 'apply':
                slug = request.POST.get('slug')
                return redirect(reverse('article_edit', args=[slug]))
            else:
                return redirect(reverse('article_index', args=[]))
        else:
            FLAG_ERROR = True
            post_data = request.POST.copy()
            for field, errors in form.errors.items():
                for error in errors:
                    if (field == 'slug' and 'Slug này đã tồn tại' in error):
                        FLAG_ERROR = False
            if (FLAG_ERROR):
                if len(form.errors) == 1 and 'tags' in form.errors:
                    errors = form.errors['tags']
                    if any("valid value" in error.lower() for error in errors):
                        del form.errors['tags']
                        article = form.save(commit=False)
                        article.save()
                        update_tags_create(request, article)
                        request.session['success_message'] = 'Thêm bài viết thành công!'
                        if request.POST.get('action') == 'submit':
                            pass
                        elif request.POST.get('action') == 'apply':
                            slug = request.POST.get('slug')
                            return redirect(reverse('article_edit', args=[slug]))
                        else:
                            return redirect(reverse('article_index', args=[]))
                    else:
                        print("Trường tags có lỗi khác.")
                else:
                    if 'tags' in form.errors:
                        errors = form.errors['tags']
                        if any("valid value" in error.lower() for error in errors):
                            del form.errors['tags']
                    request.session['error_message'] = form.errors
            else:
                post_data['slug'] = generate_unique_slug(post_data['slug'])
                new_form = ArticleForm(post_data)
                new_form.save()
                request.session['success_message'] = 'Thêm bài viết thành công!'
                if request.POST.get('action') == 'submit':
                    pass
                elif request.POST.get('action') == 'apply':
                    slug = request.POST.get('slug')
                    return redirect(reverse('category_edit', args=[slug]))
                else:
                    return redirect(reverse('category_index', args=[]))
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/article/create.html', {
        'success_message': success_message,
        'error_message': error_message,
        'category_status_choices': CATEGORY_STATUS_CHOICES,
        
        'categories': Category.objects.all(),
    })

def update_tags_edit(request, item):
    input_tags = json.loads(request.POST.get('tags', ''))
    tags_list = [tag['value'].strip() for tag in input_tags if 'value' in tag and tag['value'].strip()]    
    tag_objs = []
    for tag_name in tags_list:
        tag_slug = slugify(tag_name)
        tag_obj, created = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
        tag_objs.append(tag_obj)
    
    item.tags.set(tag_objs)


def article_edit(request, id):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    item = get_object_or_404(Article, id=id)
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            for key, value in request.POST.items():
                if hasattr(item, key):
                    if key == 'category':
                        setattr(item, key, item.category)
                    elif key != 'tags':
                        setattr(item, key, value)
            setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
            setattr(item, 'special', request.POST.get('special') == 'on')
            if 'image' in request.FILES:
                if item.image:
                    # Xóa ảnh cũ nếu có
                    old_image_path = item.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
                        # print(f"Đã xóa ảnh cũ: {old_image_path}")
                setattr(item, 'image', request.FILES['image'])
            update_tags_edit(request, item)
            item.save()
            request.session['success_message'] = 'Chỉnh sửa thành công!'
            if request.POST.get('action') == 'apply':
                request.session['FLAG_MESSAGE'] = True
                # return redirect(reverse('category_edit', args=[item.id]))
            else:
                return redirect(reverse('article_index', args=[]))
        else:
            FLAG_DELETE_IMAGE = True
            if 'image' not in request.FILES:
                image_temp = item.image
                FLAG_DELETE_IMAGE = False
                del form.errors['image']
            existSlug = True
            for field, errors in form.errors.items():
                for error in errors:
                    print('error:', error)
                    if not (field == 'slug' and 'Slug này đã tồn tại' in error):
                        request.session['error_message'] = form.errors
                        existSlug = False
            if (existSlug):
                del form.errors['slug']
                old_slug = item.slug
                for key, value in request.POST.items():
                    if hasattr(item, key):
                        if key == 'category':
                            setattr(item, key, item.category)
                        elif key != 'tags':
                            setattr(item, key, value)
                setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
                setattr(item, 'special', request.POST.get('special') == 'on')
                
                if FLAG_DELETE_IMAGE:
                    if item.image:
                        # Xóa ảnh cũ nếu có
                        old_image_path = item.image.path
                        if os.path.isfile(old_image_path):
                            os.remove(old_image_path)
                            # print(f"Đã xóa ảnh cũ: {old_image_path}")
                    image = request.FILES['image']
                    setattr(item, 'image', image)
                else:
                    print('image: ', image_temp)
                    setattr(item, 'image', image_temp)
                if (old_slug != item.slug):
                    item.slug = generate_unique_slug(item.slug)
                update_tags_edit(request, item)
                
                item.save()
                if request.POST.get('action') == 'apply':
                    request.session['FLAG_MESSAGE'] = True
                    request.session['success_message'] = 'Chỉnh sửa thành công!'

                    return redirect(reverse('article_edit', args=[item.id]))
                else:
                    return redirect(reverse('article_index', args=[]))
            else:
                request.session['FLAG_MESSAGE'] = True
                request.session['error_message'] = form.errors
    success_message = ''
    error_message = ''
    FLAG_MESSAGE = request.session.pop('FLAG_MESSAGE', False)
    if (FLAG_MESSAGE):
        success_message = request.session.pop('success_message', None)
        error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/article/edit.html', {
        'item': item,
        'success_message': success_message,
        'error_message': error_message,
        'category_status_choices': CATEGORY_STATUS_CHOICES,
        'categories': Category.objects.all(),

    })
    
def contact_index(request):
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', 'all')

    items = Contact.objects.all()
    
    if search != 'all':
        items = items.filter(name__icontains=search)

    all_count = items.count()
    contacted_count = items.filter(status='contacted').count()
    not_contacted_yet_count = items.filter(status='not contacted yet').count()
    
    if status != 'all':
        items = items.filter(status=status)
    
    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    list_status_count = {
        "all": {"count": all_count, "name": "All"},
        "contacted": {"count": contacted_count, "name": dict(CONTACT_STATUS_CHOICES)['contacted']},
        "not contacted yet": {"count": not_contacted_yet_count, "name": dict(CONTACT_STATUS_CHOICES)['not contacted yet']},
    }
    return render(request, 'myadmin/pages/contact/index.html', {
        'page_obj': page_obj,
        'list_status_count': list_status_count,
        'status': status,
    })
    
def contact_edit(request, id):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    item = get_object_or_404(Contact, id=id)
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            for key, value in request.POST.items():
                if hasattr(item, key):
                    setattr(item, key, value)

            item.save()
            request.session['success_message'] = 'Chỉnh sửa thành công!'
            if request.POST.get('action') == 'apply':
                request.session['FLAG_MESSAGE'] = True
            else:
                return redirect(reverse('contact_index_myadmin', args=[]))
        else:
            existSlug = True
            for field, errors in form.errors.items():
                for error in errors:
                    print('error:', error)
                    if not (field == 'slug' and 'Slug này đã tồn tại' in error):
                        request.session['error_message'] = form.errors
                        existSlug = False
            if (existSlug):
                # item.is_homepage = request.POST.get('is_homepage') == 'on'
                # item.layout = request.POST.get('layout')
                # item.status = request.POST.get('status')
                old_slug = item.slug
                for key, value in request.POST.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
                if (old_slug != item.slug):
                    item.slug = generate_unique_slug(item.slug)
                item.save()
                if request.POST.get('action') == 'apply':
                    request.session['FLAG_MESSAGE'] = True
                    request.session['success_message'] = 'Chỉnh sửa thành công!'

                else:
                    return redirect(reverse('contact_index_myadmin', args=[]))
            else:
                request.session['FLAG_MESSAGE'] = True
                request.session['error_message'] = form.errors
    success_message = ''
    error_message = ''
    FLAG_MESSAGE = request.session.pop('FLAG_MESSAGE', False)
    if (FLAG_MESSAGE):
        success_message = request.session.pop('success_message', None)
        error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/contact/edit.html', {
        'item': item,
        'success_message': success_message,
        'error_message': error_message,
        'contact_status_choices': CONTACT_STATUS_CHOICES,

    })
    
def tag_index(request):
    search = request.GET.get('search', 'all')

    items = Tag.objects.all()
    
    if search != 'all':
        items = items.filter(name__icontains=search)
    
    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'myadmin/pages/tag/index.html', {
        'page_obj': page_obj,
    })
    
def tag_create(request):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_message'] = 'Thêm tag thành công!'
            if request.POST.get('action') == 'submit':
                pass
            elif request.POST.get('action') == 'apply':
                slug = request.POST.get('slug')
                return redirect(reverse('category_edit', args=[slug]))
            else:
                return redirect(reverse('tag_index', args=[]))
        else:
            FLAG_ERROR = True
            for field, errors in form.errors.items():
                for error in errors:
                    if (field == 'slug' and 'Slug này đã tồn tại' in error):
                        FLAG_ERROR = False
            if (FLAG_ERROR):
                request.session['error_message'] = form.errors
            else:
                post_data = request.POST.copy()
                post_data['slug'] = generate_unique_slug(post_data['slug'])
                new_form = TagForm(post_data)
                new_form.save()
                request.session['success_message'] = 'Thêm Tag thành công!'
                if request.POST.get('action') == 'submit':
                    pass
                elif request.POST.get('action') == 'apply':
                    slug = request.POST.get('slug')
                    return redirect(reverse('category_edit', args=[slug]))
                else:
                    return redirect(reverse('tag_index', args=[]))
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/tag/create.html', {
        'success_message': success_message,
        'error_message': error_message,
    })

def tag_edit(request, id):
    if 'error_message' in request.session:
        del request.session['error_message']
    if 'success_message' in request.session:
        del request.session['success_message']
    item = get_object_or_404(Tag, id=id)
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            for key, value in request.POST.items():
                if hasattr(item, key):
                    setattr(item, key, value)

            setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
            item.save()
            request.session['success_message'] = 'Chỉnh sửa thành công!'
            if request.POST.get('action') == 'apply':
                request.session['FLAG_MESSAGE'] = True
                # return redirect(reverse('category_edit', args=[item.id]))
            else:
                return redirect(reverse('tag_index', args=[]))
        else:
            existSlug = True
            for field, errors in form.errors.items():
                for error in errors:
                    print('error:', error)
                    if not (field == 'slug' and 'Slug này đã tồn tại' in error):
                        request.session['error_message'] = form.errors
                        existSlug = False
            if (existSlug):
                old_slug = item.slug
                for key, value in request.POST.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                setattr(item, 'is_homepage', request.POST.get('is_homepage') == 'on')
                if (old_slug != item.slug):
                    item.slug = generate_unique_slug(item.slug)
                item.save()
                if request.POST.get('action') == 'apply':
                    request.session['FLAG_MESSAGE'] = True
                    request.session['success_message'] = 'Chỉnh sửa thành công!'

                    # return redirect(reverse('category_edit', args=[item.id]))
                else:
                    return redirect(reverse('tag_index', args=[]))
            else:
                request.session['FLAG_MESSAGE'] = True
                request.session['error_message'] = form.errors
    success_message = ''
    error_message = ''
    FLAG_MESSAGE = request.session.pop('FLAG_MESSAGE', False)
    if (FLAG_MESSAGE):
        success_message = request.session.pop('success_message', None)
        error_message = request.session.pop('error_message', None)
    return render(request, 'myadmin/pages/tag/edit.html', {
        'item': item,
        'success_message': success_message,
        'error_message': error_message,
        'category_status_choices': CATEGORY_STATUS_CHOICES,
        'category_layout_choices': CATEGORY_LAYOUT_CHOICES,

    })
    
def get_tags(request):
    tags = [tag.name for tag in Tag.objects.all()]
    return JsonResponse(tags, safe=False)