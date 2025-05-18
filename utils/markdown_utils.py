import markdown


def markdown_to_html(text):
    md = markdown.Markdown(extensions=["extra"])
    return md.convert(text)
