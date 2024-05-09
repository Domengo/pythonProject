"""loading PDF, DOCX and TXT files as LangChain Documents

Keyword arguments:
argument -- description
Return: return_description
"""


def load_document(file):
    """_summary_

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    import os
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None

    data = loader.load()
    return data

# splitting data in chunks


def chunk_data(data, chunk_size=256, chunk_overlap=20):
    """_summary_

    Args:
        data (_type_): _description_
        chunk_size (int, optional): _description_. Defaults to 256.
        chunk_overlap (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


# print(load_document('./1707057526924_1295665_dominicsengo.pdf'))
print(chunk_data(load_document('./1707057526924_1295665_dominicsengo.pdf')))
