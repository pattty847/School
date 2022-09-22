from transformers import pipeline

# Sentiment analysis with pipeline()
# By default, this pipeline selects a particular pretrained model that has been fine-tuned for sentiment analysis in English. 
# The model is downloaded and cached when you create the classifier object. If you rerun the command, the cached model will 
# be used instead and there is no need to download the model again.
# Available Pipelines include:     
#   feature-extraction (get the vector representation of a text)
#   fill-mask
#   ner (named entity recognition)
#   question-answering
#   sentiment-analysis
#   summarization
#   text-generation
#   translation
#   zero-shot-classification


classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")

# OUTPUT: [{'label': 'POSITIVE', 'score': 0.9598049521446228}]

# Multiple Inputs
classifier(
    ["I've been waiting for a HuggingFace course my whole life.", "I hate this so much!"]
)

# OUTPUT: [{'label': 'POSITIVE', 'score': 0.9598047137260437}, 
#           {'label': 'NEGATIVE', 'score': 0.9994558095932007}]

# Zero-shot classification
classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)

# OUTPUT: {'sequence': 
#           'This is a course about the Transformers library',
#           'labels': ['education', 'business', 'politics'],
#           'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}

# Test Generation
generator = pipeline("text-generation")
generator("In this course, we will teach you how to")

# OUTPUT: [{'generated_text': 
#           'In this course, we will teach you how to understand and use '
#           'data flow and data interchange when handling user data. We '
#           'will be working with one or more of the most commonly used '
#           'data flows — data flows of various types, as seen by the '
#           'HTTP'}]

# Multiple Models in one Pileline
generator = pipeline("text-generation", model="distilgpt2")
generator(
    "In this course, we will teach you how to",
    max_length=30,
    num_return_sequences=2,
)

# OUTPUT: [{'generated_text': 
#           'In this course, we will teach you how to manipulate the world and '
#           'move your mental and physical capabilities to your advantage.'},
# {'generated_text': 
#           'In this course, we will teach you how to become an expert and '
#           'practice realtime, and with a hands on experience on both real '
#           'time and real'}]

# Fill Mask
unmasker = pipeline("fill-mask")
unmasker("This course will teach you all about <mask> models.", top_k=2)

# OUTPUT: [{'sequence': 
#           'This course will teach you all about mathematical models.',
#           'score': 0.19619831442832947,
#           'token': 30412,
#           'token_str': ' mathematical'},
# {'sequence': 
#           'This course will teach you all about computational models.',
#           'score': 0.04052725434303284,
#           'token': 38163,
#           'token_str': ' computational'}]

# NER (Named Entity Recongnition)
ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")

# OUTPUT: [{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
#           {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
#           {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}]

# Question Answering
question_answerer = pipeline("question-answering")
question_answerer(
    question="Where do I work?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn",
)

# OUTPUT: {'score': 0.6385916471481323, 'start': 33, 'end': 45, 'answer': 'Hugging Face'}

# Summarization
summarizer = pipeline("summarization")
summarizer(
    """
    America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers.
"""
)

# OUTPUT: [{'summary_text': ' America has changed dramatically during recent years . The '
#                 'number of engineering graduates in the U.S. has declined in '
#                 'traditional engineering disciplines such as mechanical, civil '
#                 ', electrical, chemical, and aeronautical engineering . Rapidly '
#                 'developing economies such as China and India, as well as other '
#                 'industrial countries in Europe and Asia, continue to encourage '
#                 'and advance engineering .'}]

# Translation
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
translator("Ce cours est produit par Hugging Face.")

# OUTPUT: [{'translation_text': 'This course is produced by Hugging Face.'}]