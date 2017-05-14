from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

from dev.models import DevSection
from dev.models import DevPost


def index(request):
    db_sections = DevSection.objects\
        .filter(section_type=DevSection.DISCUSSION)\
        .order_by('title')
    # sections = [
    #     (section, section.devpost_set.count())
    #     for section in db_sections]
    posts = DevPost.objects\
        .filter(
            section__section_type=DevSection.DISCUSSION, 
            is_published=True)\
        .order_by('-date_published')
    sections = {}
    for post in posts:
        if post.section not in sections:
            sections[post.section] = []
        sections[post.section].append(post)
    data = [(section, post) for section, post in sections.items()]

    meta = create_meta(
        title='Guides and Tutorials',
        description='Guides and Tutorials',
        keywords=[
            'guide', 'tutorials', 'how-to', 
            'harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri())
    return render(request, 'dev/discussions/index.html', {
        'meta': meta,
        'section_type_title': 'discussions',
        # 'section_type_url': reverse('dev:discuss:index', subdomain='dev'),
        'data': data})


def dev_section(request, section): 
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.DISCUSSION)
    return render(request, 'dev/discussions/section.html', {
        'section': section,
        'posts': section.devpost_set.order_by('-date_published'),
        'section_type': 'discussions',
        # 'section_type_url': reverse('dev:discuss:index', subdomain='dev'),
        })


def dev_post(request, section, post):
    section = get_object_or_404(
        DevSection, 
        slug=section, section_type=DevSection.DISCUSSION)
    post = get_object_or_404(
        DevPost, 
        slug=post, section=section, 
        section__section_type=DevSection.DISCUSSION)
    return render(request, 'dev/discussions/post.html', {
        'meta': post.get_seo_meta(),
        'section_type': 'discussions',
        # 'section_type_url': reverse('dev:discuss:index', subdomain='dev'),
        'post': post,
        'section': section})
