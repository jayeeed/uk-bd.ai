from db.db_config import faq_ans_corpus
import os


def get_data():
    try:
        collection = faq_ans_corpus
        # Assuming you have a single document with the "text" key
        document = collection.find_one()
        if document:
            text_data = document.get("text")

            # Save the data to a text file named "ans_corpus.txt" in the current directory
            file_path = os.path.join("data", "ans_corpus.txt")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_data)

            return {"text": text_data}
        else:
            return None  # No data found
    except Exception as e:
        print(f"Error: {e}")
        return None


# this fuction posts all the ques ans after user sets or alters them
def overwrite_data(new_data):

    try:
        collection = faq_ans_corpus
        collection.delete_many({})
        collection.insert_one({"text": new_data})
        return {'message': 'Collection overwritten with new data'}

    except Exception as e:
        print(f"error_______________________{e}")
