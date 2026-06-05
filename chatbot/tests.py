from django.test import SimpleTestCase

from .services import extract_generated_text


class GeminiResponseExtractionTests(SimpleTestCase):
    def test_extract_generated_text_from_nested_parts(self):
        payload = {
            'candidates': [
                {
                    'content': {
                        'parts': [
                            {'text': 'AI finds patterns in data to make decisions.'},
                        ],
                        'role': 'model',
                    }
                }
            ]
        }

        self.assertEqual(
            extract_generated_text(payload),
            'AI finds patterns in data to make decisions.',
        )
