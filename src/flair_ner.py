import torch
from flair.data import Corpus, Dataset, Sentence
from flair.datasets import ColumnCorpus
from flair.embeddings import TransformerWordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer


def save_as_flair_fmt(data: dict[str, list[str]], filename: str):
    with open(filename, 'w') as f:
        for d in data:
            for token, label in zip(d['tokens'], d['bio_tags']):
                f.write(f"{token} {label}\n")
            f.write('\n')


def load_flair_corpus(data_path: str):
    columns = {0: 'text', 1: 'ner'}
    corpus: Corpus = ColumnCorpus(data_path, columns,
                                train_file='train.txt',
                                test_file='test.txt')
    return corpus


def train_flair_ner(corpus: Corpus, model_path: str, base_model: str = 'prajjwal1/bert-mini', max_epochs: int = 100):
    # what label do we want to predict?
    label_type = 'ner'

    # make the label dictionary from the corpus
    label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)

    # initialize fine-tuneable transformer embeddings WITH document context
    embeddings = TransformerWordEmbeddings(model=base_model,
                                        layers="-1",
                                        subtoken_pooling="first",
                                        fine_tune=True,
                                        use_context=True,
                                        )


    # initialize bare-bones sequence tagger (no CRF, no RNN, no reprojection)
    tagger = SequenceTagger(hidden_size=256,
                            embeddings=embeddings,
                            tag_dictionary=label_dict,
                            tag_type='ner',
                            use_crf=False,
                            use_rnn=False,
                            reproject_embeddings=False,
                            )

    # initialize trainer
    trainer = ModelTrainer(tagger, corpus)

    # run fine-tuning
    trainer.fine_tune(model_path,
                    learning_rate=2.0e-5,
                    mini_batch_size=25,
                    max_epochs=max_epochs,
                    use_final_model_for_eval=False,
                    )
    

def load_flair_ner(model_path: str):
    # load the model you trained
    tagger = SequenceTagger.load(model_path)
    return tagger


def flair_batch_predict(tagger: SequenceTagger, data: Dataset, batch_size: int = 4):
    with torch.no_grad():
        tagger.predict(data, mini_batch_size=batch_size)
    result = []
    for p in data:
        result.append({
            "text": p.text,
            "labels": [(span[0].idx - 1, span[-1].idx, span.labels[0].value) for span in p.get_spans()]
        })
    return result
