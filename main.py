import re
import math
import os

ngram_fast = lambda text, n: [text[i:i+n] for i in range(0, len(text) - (n-1)) if not " " in text[i:i+n]]

def count_grams(grams):
  count = dict()
  for gram in grams:
    if gram in count:
      count[gram] += 1
    else:
      count[gram] = 1

  return count

def create_digram_model(text):
  return count_grams(ngram_fast(text, 2))

def get_only_words(text):
  no_numbers = ''.join([c.lower() for c in text if not c.isdigit()])
  words = re.findall(r'\w+', no_numbers)
  return ' '.join(words)

def get_text_from_file(filename):
  with open(filename, 'r') as f:
    return f.read().replace('\n', '')

def concat_files(filenames):
  texts = map(get_text_from_file, filenames)
  text = ' '.join(texts)
  return get_only_words(text)

def create_common_model_from_files(filenames):
  text = concat_files(filenames)
  return create_digram_model(text)

def vector_len(values):
  return math.sqrt(sum([v**2 for v in values]))

def check_for_model(sample, model):
  digrams_sample = create_digram_model(get_only_words(sample))
  upp = sum([digrams_sample[gram] * model[gram] for gram in digrams_sample if gram in model])
  sample_len = vector_len(digrams_sample.values())
  model_len = vector_len(model.values())
  return 1 - (upp / (sample_len * model_len))

def check_text(sample, models):
  results = {lang: check_for_model(sample, model) for lang, model in models.items()}
  [print("for lang: ", lang, " result is: ", result) for lang, result in results.items()]
  
  print("most propable language is: ", min(results, key=results.get))

def get_lang_files():
  files = os.listdir('inputs')
  langs = dict()
  for file in files:
    l = file[:3]
    if l in langs:
      langs[l] = langs[l] + [file]
    else:
      langs[l] = [file]
  # it's hacky but files were not the point and structure can change over time
  return {lang: ['inputs/' + filename for filename in files] for lang, files in langs.items()}

def create_models():
  input_files = get_lang_files()
  return {lang: create_common_model_from_files(files) for lang, files in input_files.items()}


print("creating models...")

models = create_models()
  
print("created!")

filename = input("give filename with text to check language: ")

sample_text = get_text_from_file(filename)

check_text(sample_text, models)
