#  regex model

import re

class RegexModel:
    def __init__(self):
        self.service_pattern = None
        self.environment_pattern = None

    def fit(self, services: list[str], environments: list[str]):
        # Create regex patterns to match any service or environment
        self.service_pattern = r'\b(' + '|'.join(map(re.escape, sorted(services, key=len, reverse=True))) + r')\b'
        self.environment_pattern = r'\b(' + '|'.join(map(re.escape, sorted(environments, key=len, reverse=True))) + r')\b'

    def _tokenize(self, text: str) -> list[str]:
        return text.split()

    def _tag_matches(self, text: str, tags: list[str], pattern: str, tag_prefix: str) -> list[str]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            match_tokens = self._tokenize(match.group())
            start_idx = len(self._tokenize(text[:match.start()]))
            end_idx = start_idx + len(match_tokens) - 1
            # import pdb; pdb.set_trace()
            tags[start_idx] = f'B-{tag_prefix}'
            for i in range(start_idx + 1, end_idx + 1):
                tags[i] = f'I-{tag_prefix}'
        return tags

    def _tag_entities(self, data: list[str]) -> list[list[tuple[str, str]]]:
        tagged_sentences = []
        for line in data:
            tokens = line['tokens']
            text = ' '.join(tokens)
            tags = ['O'] * len(tokens)

            # Tag services and environments
            self._tag_matches(text, tags, self.service_pattern, 'SVC')
            self._tag_matches(text, tags, self.environment_pattern, 'ENV')

            # Combine tokens and tags
            tagged_sentence = [(token, tag) for token, tag in zip(tokens, tags)]
            tagged_sentences.append(tagged_sentence)
        return tagged_sentences

    def predict(self, data):
        return self._tag_entities(data)
