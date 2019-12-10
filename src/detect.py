def detect_document(uri):
    """Detects handwritten features in an image using Google Vision API"""
    from google.cloud import vision
    import re

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    # gets response from API
    response = client.document_text_detection(image=image)

    full_text = []

    # parses API response and displays confidence of detection
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print('Word text: {} (confidence: {})'.format(word_text, word.confidence))
                    full_text.append(word_text)

    # finds unique UVA computing ids from blocks of detected text
    # 2 or 3 letters followed by 1 digit, followed by 2 more letters
    full_text = "".join(full_text)
    ids = re.findall("[a-z]{2,3}[1-9][a-z]{2}", full_text)
    print(full_text)
    print(ids)
                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(
                            #symbol.text, symbol.confidence))

# runs on images uploaded to GCP bucket
detect_document("https://storage.googleapis.com/boardshare/img1.jpg")
