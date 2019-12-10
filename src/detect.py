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
            #print('\nBlock confidence: {}\n'.format(block.confidence))                                     

            for paragraph in block.paragraphs:
                #print('Paragraph confidence: {}'.format(paragraph.confidence))                             

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print('Word text: {} (confidence: {})'.format(word_text, word.confidence))
                    full_text.append(word_text)

                    #for symbol in word.symbols:                                                            
                        #print('\tSymbol: {} (confidence: {})'.format(#symbol.text, symbol.confidence))     

    full_text = "".join(full_text)

    # finds unique UVA computing ids from blocks of detected text                                           
    # regex matches: 2 or 3 letters, followed by 1 digit, followed by 2 more letters                        
    regex = "[a-zA-Z]{2,3}[0-9][a-zA-Z]{2}"
    email = "@virginia.edu"
    ids = re.findall(regex, full_text)
    ids_email = [id + email for id in ids]
    print(ids_email)

# runs on images uploaded to GCP bucket                                                                     
detect_document("https://storage.googleapis.com/boardshare/img3.jpg")
