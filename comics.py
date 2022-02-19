class Series:
    
    def __init__(self, url_sufix: str):
        self.url_suffix = url_sufix

    def get_issues_urls(self, issues):
        issues_urls = []

        for i in issues:
            issues_urls.append(self.url_suffix.format(issue=i))

        return issues_urls

    def get_url(self):
        return self.url_suffix