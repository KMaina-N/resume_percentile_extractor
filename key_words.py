# import nltk
# from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import fitz  # PyMuPDF for PDF handling

# nltk.download('stopwords')

# def calculate_similarity(job_description, resume):
#     # Tokenize and remove stopwords
#     stop_words = set(stopwords.words('english'))
#     job_words = nltk.word_tokenize(job_description)
#     job_words = [word.lower() for word in job_words if word.isalnum() and word.lower() not in stop_words]

#     resume_words = nltk.word_tokenize(resume)
#     resume_words = [word.lower() for word in resume_words if word.isalnum() and word.lower() not in stop_words]

#     # Convert the words into TF-IDF features
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([job_description, resume])

#     # Calculate cosine similarity between the job description and the resume
#     similarity_score = cosine_similarity(tfidf_matrix)[0, 1]

#     return similarity_score



import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('stopwords')

import fitz


def extract_keywords(text, num_keywords=5):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Convert the words into TF-IDF features
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(words)])

    # Get feature names and their corresponding TF-IDF scores
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Sort by TF-IDF scores and get the top keywords
    sorted_keywords = [feature_names[i] for i in tfidf_scores.argsort()[::-1][:num_keywords]]

    return sorted_keywords

def calculate_similarity(job_description, resume):
    # Extract keywords from the job description and resume
    job_keywords = extract_keywords(job_description)
    print(resume)
    resume_keywords = extract_keywords(resume)

    # Combine keywords into a single list
    all_keywords = list(set(job_keywords + resume_keywords))

    # Convert the keywords into TF-IDF features
    vectorizer = TfidfVectorizer(vocabulary=all_keywords)
    tfidf_matrix = vectorizer.fit_transform([job_description, resume])

    # Calculate cosine similarity between the job description and the resume
    similarity_score = cosine_similarity(tfidf_matrix)[0, 1]

    return similarity_score

# if __name__ == "__main__":
#     # Example job description
#     job_description = """
#     We are looking for a Python developer with experience in web development.
#     The ideal candidate should have strong problem-solving skills and be familiar with
#     frameworks like Django or Flask.
#     """

#     # Example resume
#     resume = """
#     I am a Python developer with extensive experience in web development.
#     I have worked with Django and Flask and have strong problem-solving skills.
#     """

#     # Calculate similarity
#     similarity_score = calculate_similarity(job_description, resume)

#     # Print the similarity score
#     print(f"Similarity Score: {similarity_score:.2%}")
if __name__ == "__main__":
    # Example job description
    job_description = open("job_description.txt", "r").read()

    # Example resume
    pdf_path = "cv_data.pdf"
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        print(page)
        text += page.get_text()
    doc.close()
    resume = text
    # print(resume)
    

    # Calculate similarity
    similarity_score = calculate_similarity(job_description, resume)

    # Print the similarity score
    print(f"Similarity Score: {similarity_score:.2%}")