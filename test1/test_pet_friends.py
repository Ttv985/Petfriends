from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()
# Тесты к библиотеке API Petfriends

# №1
'''Запрос api ключа'''
def test_get_api_key(email=valid_email, password=valid_password):
   status, result = pf.get_api_key(email, password)
   assert status == 200
   assert 'key' in result

# №2
'''Получение списка питомцев'''
def test_get_all_pets_with_valid_key(filter=''):

   _, api_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.get_list_of_pets(api_key, filter)
   assert status == 200
   assert len(result['pets']) > 0

# №3
'''Добавление питомца с верными параметрами, с фото'''
def test_add_pets_with_valid_data(name='Jill', animal_type='cat', age='3', pet_photo='images\Jill.jpg'):

   _, api_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
   assert status == 200
   assert result['name'] == name

# №4
'''Удаление питомца'''
def test_delete_pet():
   '''Проверяем возможность удаления питомца'''
   _, api_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

   if len(my_pets['pets']) == 0:
      pf.add_new_pets(api_key, 'Jane', 'cat', '5', 'images\Jil.jpg')
      _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

   pet_id = my_pets['pets'][0]['id']

   status, _ = pf.delete_pets(api_key, pet_id)
   _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

   assert status == 200
   assert pet_id not in my_pets.values()

# №5
'''Изменение данных питомца'''
def test_update_pet_info(name='Changed', animal_type='changed', age='5'):

   _, api_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

   if len(my_pets['pets']) > 0:
      status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
      assert status == 200
      assert result['name'] == name
   else:
      raise Exception("Питомцы отсутствуют")

# №6
'''Добавление питомца с верными параметрами, без фото'''
def test_add_new_pet_without_photo(name='Pad', animal_type='dog', age='6'):

   _, api_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

   assert status == 200
   assert result['name'] == name

# №7
'''Добавление фотo'''
def test_add_photo(pet_photo='images\dog.jpg'):
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
   
   _, api_key = pf.get_api_key(valid_email, valid_password)
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

   if len(my_pets['pets']) > 0:
      pet_id = my_pets['pets'][0]['id']
      status, result = pf.add_photo(auth_key, pet_id, pet_photo)

      assert status == 200
      assert 'pet_photo' in result

# №8
""" Запрос api ключа с неверным почтовым адресом"""
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):

   status, result = pf.get_api_key(email, password)

   assert status == 403

# №9
""" Запрос api ключа с пустым почтовым адресом"""
def test_get_api_key_for_empty_user(email='', password=valid_password):
   status, result = pf.get_api_key(email, password)
   assert status == 403
   assert 'Forbidden' in result

# №10
""" Запрос api ключа с пустым паролем"""
def test_get_api_key_for_empty_pasword(email=valid_email, password=''):
   status, result = pf.get_api_key(email, password)
   assert status == 403
   assert 'Forbidden' in result

# №11
"""Запрос всех питомцев c неверным фильтром"""
def test_get_all_pets_with_incorrect_filter(filter='pets'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.get_list_of_pets(auth_key, filter)
   assert status == 500
   assert 'Internal Server Error' in result

# №12
"""Запрос всех питомцев c неверным ключом"""
def test_get_all_pets_with_invalid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = auth_key['key'][::-1]
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'pets' not in result

# №13
"""Добавление фото в формате txt"""
def test_add_photo_of_pet_wrong_ext(pet_photo='images/pet.txt'):
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) == 0:
      pf.add_new_pet_without_photo(auth_key, "Cat", "Catty", "4", )
      _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
   pet_id = my_pets['pets'][0]['id']
   status, result = pf.add_photo(auth_key, pet_id, pet_photo)

   assert status != 200

# №14
"""Добавление нового питомца с пустыми параметрами"""
def test_add_new_pet_simple_empty_fields(name='', animal_type='',age=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age,)

    assert status != 200

# №15
"""Добавление нового питомца с символами в параметрах"""
def test_add_new_pet_simple_symbols(name="""!@#$%^&*(){}[]"№:;?*,/|\:"'><?/""", animal_type="""!@#$%^&*(){}[]"№:;?*,/|\:"'><?/""",age='!@'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age,)

    assert status != 200

# №16
"""Добавление нового питомца с неверным возрастом"""
def test_add_new_pet_simple_incorrect_age(name='Bob', animal_type='Dog',age='random'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age,)

    assert status != 200
