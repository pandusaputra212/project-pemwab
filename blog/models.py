from django.conf import settings
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
import os # Tambahan untuk manipulasi path file

class Post(models.Model):
    # KATEGORI BERITA PRODI
    CATEGORY_CHOICES = (
        ('pengumuman', 'Pengumuman'),
        ('akademik', 'Akademik'),
        ('kegiatan', 'Kegiatan Mahasiswa'),
        ('artikel', 'Artikel'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, verbose_name="Judul Berita")
    text = HTMLField(verbose_name="Isi Konten")

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='akademik',
        verbose_name="Kategori"
    )

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    header_image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        verbose_name="Gambar Header"
    )

    # Meta untuk mengatur perilaku model
    class Meta:
        ordering = ['-published_date'] # Berita terbaru otomatis di atas
        verbose_name = "Berita"
        verbose_name_plural = "Daftar Berita"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    # Fungsi otomatis hapus file gambar di folder media jika data di database dihapus
    def delete(self, *args, **kwargs):
        if self.header_image:
            if os.path.isfile(self.header_image.path):
                os.remove(self.header_image.path)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.CharField(max_length=200, verbose_name="Nama Pengirim")
    text = models.TextField(verbose_name="Komentar")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Daftar Komentar"

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return f"Komentar oleh {self.author} pada {self.post.title}"