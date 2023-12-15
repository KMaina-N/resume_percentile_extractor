import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF for PDF handling
import os
import shutil
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to calculate cosine similarity between two texts, description and resume
def calculate_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return similarity

# Function to preprocess text using spaCy
def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

# Sample job description
job_description = open("job_description.txt", "r").read()

file_scores = {}
# Sample resumes
resume_paths = 'resumes'
resume_files = os.listdir(resume_paths)
for resume_file in resume_files:
    resume_path = os.path.join(resume_paths, resume_file)
    resume_text = extract_text_from_pdf(resume_path)
    print('------------------------------------------------------')
    job_description_processed = preprocess_text(job_description)
    resume_processed = preprocess_text(resume_text)
    similarity_score = calculate_similarity(job_description_processed, resume_processed)
    print(f"Similarity Score (Resume) {resume_file}: {similarity_score:.1%}")
    round(similarity_score, 2)*100

    # add to scores the filename and similarity score
    file_scores[resume_file] = similarity_score

def get_top_percent(threshold_value):
    print(threshold_value)
    scores = file_scores.values()
    sorted_values = sorted(scores, reverse=True)
    # Calculate the index for the top % cutoff with a minimum value of 1
    # threshold_value = 0.50
    top_percent_index = max(1, int(threshold_value * len(scores)))
    # Retrieve the top 5% values
    top_percent_values = sorted_values[:top_percent_index]
    # move the files to the top qualified folder
    for i in top_percent_values:
        print(i)
        for k, v in file_scores.items():
            if v == i:
                print(k)
                shutil.copy('resumes/' + k, 'top_qualified/' + k)
                os.remove('resumes/' + k)

if __name__ == '__main__':
    threshold = (input('Threshold: '))
    threshold = float(threshold)
    get_top_percent(threshold)