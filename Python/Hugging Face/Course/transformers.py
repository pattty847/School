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