import argparse
import jieba
import jieba.analyse
from gensim import corpora, models
from tqdm import tqdm
import pandas as pd


def extract_keywords(sentence, topK_num):
    # Basic keyword extraction
    basic_keywords = " ".join(jieba.analyse.extract_tags(sentence=sentence, topK=topK_num, withWeight=False))
    print("Basic Keywords:")
    print(basic_keywords)

    # Keyword extraction with part-of-speech filtering, extracting nouns and verbs
    pos_keywords = jieba.analyse.extract_tags(sentence, topK=topK_num, withWeight=True, allowPOS=(["n", "v"]))
    print("\nKeywords with POS (nouns and verbs) and Weights:")
    print(pos_keywords)

    # Using TextRank algorithm for keyword extraction
    textrank_result = " ".join(jieba.analyse.textrank(sentence, topK=topK_num, withWeight=False, allowPOS=("ns", "n", "vn", "v")))
    print("\nKeywords using TextRank:")
    print(textrank_result)


def extract_topics_from_data(sentence, stop_words, num_topics=10, words_per_topic=8):
    # Load stopwords
    stopwords = pd.read_csv(stop_words, index_col=False, quoting=3, sep="\t", names=["stopword"], encoding="utf-8")
    stopwords = stopwords["stopword"].values

    # Preprocess the sentence
    segs = jieba.lcut(sentence)
    segs = [v for v in segs if not str(v).isdigit()]  # Remove digits
    segs = list(filter(lambda x: x.strip(), segs))  # Remove spaces
    segs = list(filter(lambda x: x not in stopwords, segs))  # Remove stopwords

    sentences = [segs]  # Prepare the list of sentences for LDA

    # Build dictionary and corpus
    dictionary = corpora.Dictionary(sentences)
    corpus = [dictionary.doc2bow(sentence) for sentence in sentences]

    # LDA model
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)

    # Print topics
    for topic in lda.print_topics(num_topics=num_topics, num_words=words_per_topic):
        print(topic[1])


def main():
    parser = argparse.ArgumentParser(description="Extract keywords and topics from text using jieba and gensim.")
    parser.add_argument("-s", "--sentence", type=str, help="Sentence from which to extract keywords or topics.")
    parser.add_argument("-k", "--topK_num", type=int, default=10, help="Number of top keywords or topics to extract.")
    parser.add_argument("-sw", "--stopwords", type=str, help="File path for stopwords.")
    args = parser.parse_args()

    if args.sentence:
        extract_keywords(args.sentence, args.topK_num)
        if args.stopwords:
            extract_topics_from_data(args.sentence, args.stopwords, num_topics=args.topK_num)


if __name__ == "__main__":
    main()
