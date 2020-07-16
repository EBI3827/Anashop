from django.shortcuts import render, reverse
from django.views.generic import DetailView, ListView, View
from .models import Blog, BlogComment
from .forms import BlogCommentForm
from django.views.generic.edit import FormMixin
from star_ratings.models import Rating
from .models import Blog
from taggit.models import Tag

# Create your views here.


class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class BlogDetailView(FormMixin, DetailView):
    model = Blog
    template_name = 'blog-detail.html'
    form_class = BlogCommentForm

    def get_success_url(self):
        return reverse('blog:blog-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = BlogCommentForm(initial={'blog': self.object})
        context['comments'] = self.object.comments.filter(
            approved=True, parent=None).order_by('-date')
        context['rating'] = Rating.objects.get(
            object_id=self.object.id, content_type__model='‌Blog')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = BlogComment.objects.get(id=parent_id)
                replay_comment = form.save(commit=False)
                # assign parent_obj to replay comment
                replay_comment.parent = parent_obj
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(BlogDetailView, self).form_valid(form)
