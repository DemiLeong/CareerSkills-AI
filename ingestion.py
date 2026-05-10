import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------
# Folder Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "db")


# -----------------------------
# Build Vector Database
# -----------------------------

def build_vector_db(folder_name):

    print(f"\nBuilding vector DB for: {folder_name}")

    folder_path = os.path.join(DATA_DIR, folder_name)
    save_path = os.path.join(DB_DIR, folder_name)

    # Load all txt files
    loader = DirectoryLoader(
        folder_path,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector DB
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Save DB
    vectorstore.save_local(save_path)

    print(f"Saved vector DB → {save_path}")
    print("-" * 50)


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    os.makedirs(DB_DIR, exist_ok=True)

    build_vector_db("jobs")
    build_vector_db("courses")
    build_vector_db("resume_samples")
    build_vector_db("policy")

    print("\n✅ ALL VECTOR DATABASES CREATED SUCCESSFULLY")