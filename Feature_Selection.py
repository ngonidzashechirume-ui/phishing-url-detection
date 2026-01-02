# Drop non-feature columns
from filter import african_urls

X = african_urls.drop(columns=['FILENAME', 'URL', 'Domain', 'Title', 'label'])

# Target column
y = african_urls['label']
