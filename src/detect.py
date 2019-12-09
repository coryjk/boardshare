def detect_document(uri):
    """Detects document features in an image."""
    from google.cloud import vision
    import re

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    full_text = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    full_text.append(word_text)
    full_text = "".join(full_text)
    ids = re.findall("[a-zA-Z]{2,3}[0-9][a-zA-Z]{2,3}", full_text)
    print(full_text)
    print(ids)
                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(
                            #symbol.text, symbol.confidence))


detect_document("https://storage.googleapis.com/boardshare/img1.jpg")
