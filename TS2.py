
import nltk
import numpy as np
import networkx as nx

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    sentences = nltk.sent_tokenize(text)
    words = [word_tokenize(sent) for sent in sentences]
    tagged_words = [nltk.pos_tag(word) for word in words]
    return sentences, tagged_words

def is_valid_word(word):
    valid_pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']
    return word[1] in valid_pos and len(word[0]) > 1

def build_graph(tagged_words):
    graph = nx.Graph()
    for i, word in enumerate(tagged_words):
        if is_valid_word(word):
            for j in range(i + 1, len(tagged_words)):
                if is_valid_word(tagged_words[j]):
                    graph.add_edge(word[0], tagged_words[j][0])
    return graph

def textrank(graph):
    return nx.pagerank(graph)

def sentence_similarity(sentence1, sentence2):
    stopwords_en = set(stopwords.words('english'))
    words1 = [word.lower() for word in word_tokenize(sentence1) if word.lower() not in stopwords_en]
    words2 = [word.lower() for word in word_tokenize(sentence2) if word.lower() not in stopwords_en]
    common_words = set(words1) & set(words2)
    return len(common_words) / (np.log(len(words1)) + np.log(len(words2)) + 1)

def build_sentence_graph(sentences):
    graph = nx.Graph()
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = sentence_similarity(sentences[i], sentences[j])
            if similarity > 0:
                graph.add_edge(i, j, weight=similarity)
    return graph

def summarize(text, num_sentences=3):
    sentences, tagged_words = preprocess_text(text)
    sentence_graph = build_sentence_graph(sentences)
    scores = nx.pagerank(sentence_graph, weight='weight')
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    summarized_text = ' '.join([sentence for score, sentence in ranked_sentences[:num_sentences]])
    return summarized_text

# Example usage
text = """
Title: "The Legacy of Kindness"

In a small village nestled between lush green hills, there lived an elderly woman named Mrs. Thompson. She was known far and wide for her kindness and generosity. Every day, Mrs. Thompson would bake bread and distribute it among the needy, visit the sick, and offer a helping hand to anyone in need. Her acts of kindness had touched the hearts of everyone in the village.

One day, a young traveler named Ethan arrived in the village. He was tired, hungry, and had lost his way in the dense forest. Desperate for help, Ethan stumbled upon Mrs. Thompson's humble cottage. With a warm smile, she welcomed him inside, offering him food, shelter, and guidance.

As days turned into weeks, Ethan became enchanted by Mrs. Thompson's selflessness and compassion. He learned from her the true meaning of kindness and the importance of helping others without expecting anything in return.

Before departing, Ethan asked Mrs. Thompson, "How can I repay you for your kindness?"

Mrs. Thompson simply replied, "Pass it on, my dear. Spread kindness wherever you go."

Inspired by Mrs. Thompson's words, Ethan embarked on a journey to spread kindness and compassion. Everywhere he went, he shared Mrs. Thompson's teachings, helping those in need and encouraging others to do the same.

Years passed, and Ethan became an influential figure, known for his acts of kindness and generosity. His legacy of compassion echoed far and wide, touching the lives of countless people.

Meanwhile, back in the village, Mrs. Thompson's health began to decline. Despite her frailty, she continued to spread love and kindness to those around her.

One day, Ethan returned to the village to find Mrs. Thompson lying on her bed, surrounded by villagers whose lives she had touched. With tears in his eyes, Ethan thanked her for the impact she had made on his life and the lives of so many others.

Mrs. Thompson smiled weakly and whispered, "Remember, kindness is the greatest gift we can give to the world."

After Mrs. Thompson's passing, the villagers came together to honor her memory. They built a monument in the village square, inscribed with the words: "In loving memory of Mrs. Thompson, whose kindness touched the lives of many."

The legacy of Mrs. Thompson's kindness lived on through Ethan and the villagers, reminding everyone of the power of compassion to create a better world for all.

Moral:
The story underscores the profound impact of kindness and compassion on individuals and communities. It teaches us that acts of kindness, no matter how small, have the power to transform lives and leave a lasting legacy. Furthermore, it emphasizes the importance of paying forward kindness, spreading goodwill, and nurturing a culture of empathy and generosity.
"""

summary = summarize(text)
print("Summary:")
print(summary)
