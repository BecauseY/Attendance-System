import face_recognition


def face_identify(name_id):
    rva = '.\\static\\face\\'
    pic_format = '.jpg'
    addr_photo = rva + name_id + pic_format
    picture_of_me = face_recognition.load_image_file(addr_photo)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    rva = '.\\static\\pic\\'
    pic_format = '.png'
    addr_photogra = rva + name_id + pic_format
    unknown_picture = face_recognition.load_image_file(addr_photogra)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0]:
        return True
    else:
        return False
