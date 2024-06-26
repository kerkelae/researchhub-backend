import datetime
import re

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from markdown import markdown

from researchhub_document.models import ResearchhubPost


def markdown_to_text(markdown_string):
    """Converts a markdown string to plaintext"""

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r"<pre>(.*?)</pre>", " ", html)
    html = re.sub(r"<code>(.*?)</code >", " ", html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = "".join(soup.findAll(text=True))

    return text


class Command(BaseCommand):
    def handle(self, *args, **options):
        needs_text = ResearchhubPost.objects.filter(renderable_text="")
        count = needs_text.count()
        for i, post in enumerate(needs_text):
            print("{} / {} / id: {}".format(i, count, post.id))
            md = post.get_full_markdown()
            if md:
                print("in md: {}".format(md))
                text = markdown_to_text(md)
                if len(text) > 255:
                    text = text[0:255] + "..."
                post.renderable_text = text
                post.save()
                print("{} / {} markdown saved".format(i, count))
