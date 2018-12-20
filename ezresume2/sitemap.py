from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # need to map static pages
        return ['home', 'privacy', 'login', 'register']

    def location(self, item):
        return reverse(item)
