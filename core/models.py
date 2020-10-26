from django.db import models
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('3', '3D'), ('EC', 'E-commerce'), ('AG', 'Agency'), ('AP', 'App'),
    ('BC', 'Blockchain'), ('BG', 'Blog'), ('BK', 'Book'), ('BS', 'Business'),
    ('CS', 'Coming Soon'), ('CM', 'Community'), ('CO', 'Corporate'),
    ('CR', 'Creative'), ('CC', 'Cryptocurrency'), ('CL', 'Culture'),
    ('DS', 'Design Tools'), ('DV', 'Development Tools'), ('ED', 'Education'),
    ('EN', 'Entertainment'), ('EV', 'Event'), ('FS', 'Fashion'), ('FN', 'Finance'),
    ('FD', 'Food & Drinks'), ('FI', 'Furniture & Interiors'), ('GR', 'Gradient'),
    ('HF', 'Health & Fitness'), ('HT', 'Hosting'), ('IL', 'Illustration'),
    ('IN', 'Insurance'), ('IS', 'Isometric'), ('MG', 'Magazine'), ('MN', 'Minimal'),
    ('MS', 'Miscellaneous'), ('OT', 'Outdoors & Travel'), ('PN', 'Pattern'),
    ('PG', 'Photography'), ('PF', 'Portfolio'), ('PM', 'Product Management'),
    ('PD', 'Productivity'), ('PT', 'Prototype'), ('RE', 'Real Estate'),
    ('SW', 'Software'), ('SD', 'Studio'), ('TC', 'Technology'), ('TG', 'Typography')
)

COLOR_CHOICES = (
    ('AQ', 'Aqua'), ('BK', 'Black'), ('BL', 'Blue'), ('BR', 'Brown'),
    ('GR', 'Gray'), ('GN', 'Green'), ('LM', 'LIME'), ('MR', 'Maroon'),
    ('ML', 'Multiple Colors'), ('NV', 'Navy'), ('OL', 'Olive'),
    ('OR', 'Orange'), ('PN', 'Pink'), ('PR', 'Purple'), ('RD', 'Red'),
    ('TL', 'Teal'), ('UV', 'Ultra Violet'), ('WT', 'White'),
    ('YL', 'Yellow')
)


class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    color = models.CharField(choices=COLOR_CHOICES, max_length=2)
    image_url = models.CharField(max_length=2000)
    date_added = models.DateField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:website', kwargs={'slug': self.slug})
    
    def get_save_to_profile_url(self):
        return reverse('core:save_to_profile', kwargs={'slug': self.slug})

    def get_remove_from_profile_url(self):
        return reverse('core:remove_from_profile', kwargs={'slug': self.slug})


class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.website.title


class SavedWebsites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    websites = models.ManyToManyField(Save)
    saved = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
