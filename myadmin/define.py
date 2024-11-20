CATEGORY_STATUS_CHOICES = [
    ('published', 'Published'),
    ('draft', 'Draft'),
    ('pending', 'Pending'),
]

ARTICLE_STATUS_CHOICES = [
    ('published', 'Published'),
    ('draft', 'Draft'),
    ('pending', 'Pending'),
]

CONTACT_STATUS_CHOICES = [
    ('contacted', 'Contacted'),
    ('not contacted yet', 'Not contacted yet'),
]

CATEGORY_LAYOUT_CHOICES = {
    ("grid", "Grid"),
    ("list", "List"),
}


CATEGORY_STATUS_DEFAULT = next((value for value, label in CATEGORY_STATUS_CHOICES if value == 'draft'), None)
ARTICLE_STATUS_DEFAULT = next((value for value, label in ARTICLE_STATUS_CHOICES if value == 'draft'), None)
CONTACT_STATUS_DEFAULT = next((value for value, label in CONTACT_STATUS_CHOICES if value == 'not contacted yet'), None)
CATEGORY_LAYOUT_DEFAULT = next((value for value, label in CATEGORY_LAYOUT_CHOICES if value == 'list'), None)


