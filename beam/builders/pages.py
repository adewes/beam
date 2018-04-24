from .base import BaseBuilder

class PagesBuilder(BaseBuilder):

    def __init__(self, site):
        super().__init__(site)
        self.pages_by_language = {}

    def index(self, params, language):
        pages = self.parse_pages(params.get('pages', []), language)
        self.pages_by_language[language] = pages
        links = self.create_links(pages, language)
        return {
            'links' : links,
            'vars' : {
                'pages' : pages
            }
        }

    def create_links(self, pages, language):
        links = {}
        for page in pages:
            if not 'src' in page:
                continue
            links[page['name']] = page['dst']
            if page.get('index'):
                links[''] = page['dst']
        return links

    def build(self):
        for language, pages in self.pages_by_language.items():
            for page in pages:
                if not 'src' in page:
                    continue
                self.build_page(page, language)

    def build_page(self, page, language):
        vars = {
            'page' : page,
        }
        input = self.site.load(page['src'])
        output = self.site.process(input, page, vars, language)
        filename = self.site.get_filename(language, page['name'])
        self.site.write(output, filename)

    def flatten_pages(self, pages):
        """
        Flattens the page hierarchy into a single list, replacing the
        names to reflect the page structure.
        """
        flat_pages = []
        def add_pages(pages, prefix):
            for page in pages:
                new_page = page.copy()
                new_page['children'] = []
                if prefix:
                    new_page['name'] = '.'.join(prefix+[new_page['name']])
                flat_pages.append(new_page)
                if 'children' in page:
                    add_pages(page['children'], prefix+[page['name']])
        add_pages(pages, [])
        return flat_pages 

    def parse_pages(self, pages, language):
        flat_pages = self.flatten_pages(pages)
        pages = self.site.parse_objs(flat_pages, language)
        page_index = {page['name'] : page for page in pages}
        new_slugs = {}
        #we parse child pages and generate appropriate links
        for page in pages:
            components = page['name'].split('.')
            if len(components) > 1:
                full_slug = []
                for i in range(1, len(components)+1):
                    name = '.'.join(components[:i])
                    if name in page_index:
                        full_slug.append(page_index[name]['slug'])
                new_slugs[page['name']] = '/'.join(full_slug)
                page['level'] = len(components)-1
                parent = '.'.join(components[:-1])
                if parent in page_index:
                    parent_page = page_index[parent]
                    page['parent'] = parent_page
                    if not 'children' in parent_page:
                        parent_page['children'] = []
                    parent_page['children'].append(page)
                else:
                    logger.warning("No parent found for page {}".format(page['name']))
            else:
                page['level'] = 0
        #we update the slugs for the child pages
        for name, slug in new_slugs.items():
            page = page_index[name]
            page['slug'] = slug
            page['dst'] = self.site.get_dst(slug, language)
        return pages