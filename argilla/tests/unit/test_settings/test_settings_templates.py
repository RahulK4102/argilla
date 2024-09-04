# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from unittest import mock
from datasets import Dataset, Features, Value, ClassLabel, Sequence

import argilla as rg
from argilla.settings._templates import DefaultSettingsMixin


class TestDefaultSettingsMixin:
    def test_for_document_classification(self):
        mock_labels = ["positive", "negative"]
        settings = DefaultSettingsMixin.for_document_classification(labels=mock_labels)
        assert settings.guidelines == "Select a label for the document."
        assert len(settings.fields) == 1
        assert settings.fields[0].name == "text"
        assert len(settings.questions) == 1
        assert settings.questions[0].name == "label"
        assert settings.questions[0].labels == mock_labels

    def test_for_response_ranking(self):
        settings = DefaultSettingsMixin.for_response_ranking()
        assert settings.guidelines == "Rank the responses."
        assert len(settings.fields) == 3
        assert settings.fields[0].name == "instruction"
        assert settings.fields[1].name == "response1"
        assert settings.fields[2].name == "response2"
        assert len(settings.questions) == 1
        assert settings.questions[0].name == "ranking"
        assert settings.questions[0].values == ["response1", "response2"]

    def test_for_response_rating(self):
        settings = DefaultSettingsMixin.for_response_rating()
        assert settings.guidelines == "Rate the response."
        assert len(settings.fields) == 2
        assert settings.fields[0].name == "instruction"
        assert settings.fields[1].name == "response"
        assert len(settings.questions) == 1
        assert settings.questions[0].name == "rating"
        assert settings.questions[0].values == [1, 2, 3, 4, 5]


class TestAutoSettings:
    def test_from_text_classification_dataset(self):
        text_classification_dataset = Dataset.from_dict(
            {
                "text": ["This is a test", "This is another test"],
                "label": ["pos", "neg"],
            },
            features=Features(
                {
                    "text": Value(dtype="string", id=None),
                    "label": ClassLabel(names=["neg", "pos"], id=None),
                }
            ),
        )
        settings = rg.Settings.from_dataset(text_classification_dataset, labels=["pos", "neg"])

    def test_from_response_ranking_dataset(self):
        response_rating_dataset = Dataset.from_dict(
            {
                "prompt": ["This is a test", "This is another test"],
                "chosen": [
                    {"content": "this is a test", "role": "pos"},
                    {"content": "this is a test", "role": "pos"},
                ],
                "rejected": [
                    {"content": "this is another test", "role": "neg"},
                    {"content": "this is a test", "role": "pos"},
                ],
            },
            features=Features(
                {
                    "prompt": Value(dtype="string"),
                    "chosen": Sequence(
                        feature={
                            "content": Value(dtype="string"),
                            "role": Value(dtype="string"),
                        }
                    ),
                    "rejected": Sequence(
                        feature={
                            "content": Value(dtype="string"),
                            "role": Value(dtype="string"),
                        }
                    ),
                }
            ),
        )
        settings = rg.Settings.from_dataset(response_rating_dataset)

    def test_from_response_rating_dataset(self):
        response_rating_dataset = Dataset.from_dict(
            {
                "instruction": ["This is a test", "This is another test"],
                "input": ["this is a test", "this is another test"],
                "output": ["this is a test", "this is another test"],
            },
            features=Features(
                {
                    "instruction": Value("string"),
                    "input": Value("string"),
                    "output": Value("string"),
                }
            ),
        )
        settings = rg.Settings.from_dataset(response_rating_dataset)