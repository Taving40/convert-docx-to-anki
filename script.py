from docx import Document
import os

def ensure_file_exists(filepath):
    """Check if the file exists, and if not, create it."""
    if not os.path.exists(filepath):
        open(filepath, 'w').close()
    return filepath
    
def handle_newlines(paragraphs):
    # Initialize an empty list to hold the final result
    result = []

    # Iterate over each paragraph in the original list
    for paragraph in paragraphs:
        # Split the paragraph by '\n' and extend the result list
        result.extend(paragraph.split('\n'))

    # Print the result
    return result

def convert_doc(doc_title):

    # Load the .docx file
    doc = Document(doc_title)
    
    # Extract a mutable list of the text paragraphs
    paragraphs = handle_newlines([p.text for p in doc.paragraphs])
    
    # TODO: remove
    # with open(ensure_file_exists('test.txt'), 'w', encoding='utf-8') as f:
        # for i in range(len(paragraphs)):
            # f.write(f'{i} {paragraphs[i]}'.replace('\n', 'NEWLINE'))
            # f.write('\n')

    # Initialize an empty list to hold question-answer pairs
    qa_pairs = []

    # Temporary variables to store the current question and answer
    current_question = ""
    current_answer = ""
    empty_line_count = 0
    (i, j) = (0, 0)

    while i < len(paragraphs):
        print()
        print(paragraphs[i].encode("utf-8"), (i, j))
        print()
        if paragraphs[i]: 
            empty_line_count = 0
        else:
            empty_line_count += 1
        if empty_line_count >= 2:
            current_question = ""
            current_answer = ""
            
        if not paragraphs[i]:
            print("empty space, moving on...", (i, j))
            i += 1
            continue
        
        # once we are sure we have text, check for newline character
        
        # find all of a question
        if paragraphs[i] and not current_question:
            print()
            print(f"we dont have q, adding current text as q", (i, j))
            print()
            current_question = paragraphs[i]
            j = i+1
            while j < len(paragraphs) and paragraphs[j]:
                print(f"we found a continuation of a question, appending to curr question: {paragraphs[j]}".encode("utf-8"), (i, j))
                current_question += f"<br>{paragraphs[j]}"
                j += 1
            i = j
            continue
        
        # find all of an answer
        if paragraphs[i] and current_question:
            print()
            print(f"we have q: {current_question}, adding current text as answer".encode("utf-8"), (i, j))
            print()
            current_answer = paragraphs[i]
            j = i+1
            while j < len(paragraphs) and paragraphs[j]:
                print()
                print(f"we found a continuation of an answer, appending to curr answer: {paragraphs[j]}".encode("utf-8"), (i, j))
                print()
                current_answer += f"<br>{paragraphs[j]}"
                j += 1
            i = j
            # write down the pair
            if current_question and current_answer:
                print()
                print(f"added pair: {current_question}    ;    {current_answer}".encode("utf-8"), (i, j))
                print()
                qa_pairs.append(f"{current_question};{current_answer}")
                current_question = ""
                current_answer = ""
            continue
            
        i += 1
        
    # Path to the output .txt file
    output_file_path = f'{doc_title[:-5]}.txt'

    # Ensure the file exists or create it
    ensure_file_exists(output_file_path)

    # Write the question-answer pairs to a .txt file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for pair in qa_pairs:
            f.write(pair + '\n')

docx_files = [f for f in os.listdir('./') if f.endswith('.docx') and not f.startswith('~')]
print()
print([f.encode("utf-8") for f in docx_files])
print()


[convert_doc(doc) for doc in docx_files]
