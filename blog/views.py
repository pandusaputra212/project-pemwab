from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Untuk logika pencarian kompleks
from .models import Post 
from .forms import PostForm, CommentForm

# --- HALAMAN STATIS ---

def landing(request):
    # Mengambil 3 berita terbaru untuk ditampilkan di landing page (jika perlu)
    latest_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
    return render(request, 'blog/landing.html', {'latest_posts': latest_posts})

def about(request):
    return render(request, 'blog/about.html')

# --- LOGIKA BERITA (POST) ---

def post_list(request): 
    query = request.GET.get('q') # Mengambil input dari form pencarian
    
    # Filter dasar: Hanya yang sudah dipublish
    posts = Post.objects.filter(published_date__lte=timezone.now())
    
    if query:
        # Mencari di judul atau di isi teks berita
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(text__icontains=query)
        )
    
    # Urutkan berdasarkan yang terbaru (tanda minus '-' berarti descending)
    posts = posts.order_by('-published_date') 
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'query': query # Mengirim kembali kata kunci ke template untuk ditampilkan
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# --- LOGIKA ADMIN (CRUD) ---

@login_required
def post_new(request):
    if request.method == "POST":
        # Menambahkan request.FILES untuk mendukung upload gambar
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'title': 'Tambah Berita Baru'})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # Tambahkan request.FILES agar gambar lama bisa diganti
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'title': 'Edit Berita'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# --- AUTENTIKASI ---

def custom_logout(request):
    logout(request)
    return redirect('/')

# --- KOMENTAR ---

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})