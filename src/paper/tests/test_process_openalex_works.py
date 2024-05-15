import json

from rest_framework.test import APITestCase

from paper.models import Paper
from paper.openalex_util import process_openalex_works
from researchhub_document.related_models.researchhub_unified_document_model import (
    ResearchhubUnifiedDocument,
    UnifiedDocumentConcepts,
)
from tag.models import Concept
from topic.models import Topic, UnifiedDocumentTopics


class ProcessOpenAlexWorksTests(APITestCase):
    def setUp(self):
        with open("./paper/tests/openalex_works.json", "r") as file:
            response = json.load(file)
            self.works = response.get("results")

    def test_create_papers_from_openalex_works(self):
        process_openalex_works(self.works)

        dois = [work.get("doi") for work in self.works]
        dois = [doi.replace("https://doi.org/", "") for doi in dois]

        created_papers = Paper.objects.filter(doi__in=dois)
        self.assertEqual(len(created_papers), 2)

    def test_creating_papers_should_create_related_topics(self):
        process_openalex_works(self.works)

        dois = [work.get("doi") for work in self.works]
        dois = [doi.replace("https://doi.org/", "") for doi in dois]
        created_papers = Paper.objects.filter(doi__in=dois)

        # Sample the first paper to ensure it has concepts
        paper_concepts = created_papers.first().unified_document.concepts.all()
        self.assertGreater(len(paper_concepts), 0)

    def test_creating_papers_should_create_related_concepts(self):
        process_openalex_works(self.works)

        dois = [work.get("doi") for work in self.works]
        dois = [doi.replace("https://doi.org/", "") for doi in dois]
        created_papers = Paper.objects.filter(doi__in=dois)

        # Sample the first paper to ensure it has topics
        paper_topics = created_papers.first().unified_document.topics.all()
        self.assertGreater(len(paper_topics), 0)

    def test_creating_papers_should_create_related_hubs(self):
        process_openalex_works(self.works)

        dois = [work.get("doi") for work in self.works]
        dois = [doi.replace("https://doi.org/", "") for doi in dois]
        created_papers = Paper.objects.filter(doi__in=dois)

        # Sample the first paper to ensure it has topics
        paper_hubs = created_papers.first().unified_document.hubs.all()
        self.assertGreater(len(paper_hubs), 0)

    def test_updating_existing_papers_from_openalex_works(self):
        # First create paper
        work = self.works[0]
        work["title"] = "Old title"
        process_openalex_works([work])

        # Update paper
        work["title"] = "New title"
        process_openalex_works([work])

        dois = [work.get("doi") for work in self.works]
        dois = [doi.replace("https://doi.org/", "") for doi in dois]
        updated_paper = Paper.objects.filter(doi__in=dois).first()

        self.assertEqual(updated_paper.title, "New title")
        self.assertEqual(updated_paper.paper_title, "New title")
