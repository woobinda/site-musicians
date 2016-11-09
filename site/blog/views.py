from django.shortcuts import render
from .models import Article, Category, Tag, Comment
from django.views.generic import CreateView
from .forms import CommentForm

category_list = Category.objects.order_by('name')  # common filters
tag_list = Tag.objects.order_by('name')


def blog_view(request, categoryslug=None, tagslug=None):
    title = "Blog"
    blog_list = Article.objects.filter(status='P').order_by('-created_date')

    if categoryslug:
        blog_list = blog_list.filter(category__slug=categoryslug)
        title = Category.objects.get(slug=categoryslug)

    if tagslug:
        blog_list = blog_list.filter(tags__slug=tagslug)
        title = Tag.objects.get(slug=tagslug)

    def count(count=0):
        for article in blog_list:
            if article:
                count += 1
        return count

    return render(request, 'blog/blog_index.html',
                  {'title': title, 'blog_list': blog_list, 'category_list': category_list, 'tag_list': tag_list,
                   'count': count()})


class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/article_detail.html'
    form_class = CommentForm

    def dispatch(self, *args, **kwargs):
        return super(ArticleDetail, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        if form['parent'].value() != '':
            parent = Comment.objects.get(id=int(form['parent'].value()))
            instance.parent = parent
        instance.user = self.request.user
        instance.author_name = self.request.user.username
        instance.save()
        return super(ArticleDetail, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ArticleDetail, self).get_form_kwargs()
        kwargs['article'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        d = super(ArticleDetail, self).get_context_data(**kwargs)
        articlec = self.get_object()
        d['title'] = Article.objects.get(title=articlec)
        d['comment_tree'] = Comment.objects.select_related().filter(article=articlec).filter(parent=None).order_by(
            'path')
        d['category_list'] = category_list
        d['tag_list'] = tag_list
        d['article'] = articlec
        d['article'].views += 1
        d['article'].save()
        return d

    def get_success_url(self):
        return self.get_object().get_absolute_url()
