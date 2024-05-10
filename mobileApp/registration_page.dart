import 'dart:convert';

import 'package:finance_app/main_page.dart';
import './constants.dart' as url_file;
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Gender {
  final String ukr;
  final String abr;

  Gender(
      {required this.ukr,
        required this.abr});
}

class RegistrationPage extends StatefulWidget {
  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  final _formKey = GlobalKey<FormState>();
  Gender? _gender;
  TextEditingController _nameController = TextEditingController();
  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  TextEditingController _birthDateController = TextEditingController();
  int registrationStatusCode = -1;
  final List<Gender> genders = [Gender(ukr: 'Чоловіча', abr: 'M'), Gender(ukr: 'Жіноча', abr: 'F'), Gender(ukr: 'Інше', abr: 'A')];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Реєстрація користувача'),
      ),
      body: SingleChildScrollView(
        child: Container(
          padding: EdgeInsets.all(20.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                TextFormField(
                  controller: _nameController,
                  decoration: InputDecoration(labelText: 'Ім\'я'),
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть ім\'я';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _emailController,
                  decoration: InputDecoration(labelText: 'Email'),
                  validator: (value) {
                    if (value!.isEmpty || !value!.contains('@')) {
                      return 'Будь ласка, введіть дійсну електронну адресу';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _passwordController,
                  decoration: InputDecoration(labelText: 'Пароль'),
                  obscureText: true,
                  validator: (value) {
                    if (value!.isEmpty || value!.length < 6) {
                      return 'Пароль повинен містити принаймні 6 символів';
                    }
                    return null;
                  },
                ),
                DropdownButtonFormField<Gender>(
                  value: _gender,
                  items: genders.map((gender) {
                    return DropdownMenuItem<Gender>(
                      value: gender,
                      child: Text(gender.ukr),
                    );
                  }).toList(),
                  onChanged: (Gender? value) {
                    setState(() {
                      _gender = value!;
                    });
                  },
                  validator: (value) {
                    if (value == null) {
                      return 'Будь ласка, виберіть стать';
                    }
                    return null;
                  },
                  decoration: InputDecoration(labelText: 'Стать:'),
                ),
                TextFormField(
                  controller: _birthDateController,
                  decoration: InputDecoration(labelText: 'Дата народження'),
                  keyboardType: TextInputType.datetime,
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть дату народження';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 20.0),
                ElevatedButton(
                  onPressed: () async {
                    if (_formKey.currentState!.validate()) {
                      await _submitForm(_nameController.text, _emailController.text, _passwordController.text, _gender!.abr, _birthDateController.text);
                      if (registrationStatusCode == 201) {
                        Navigator.of(context).pushReplacement(
                            MaterialPageRoute(
                                builder: (context) => BudgetPlanningPage()));
                        showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: const Text(
                                  'Your successfully registered!'),
                              content: const Text('You can plan your budget'),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                  },
                                  child: const Text('OK'),
                                ),
                              ],
                            );
                          },
                        );
                      } else if (registrationStatusCode != -1) {
                        showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: const Text('Registration Failed'),
                              content: Text(
                                  'Status code: $registrationStatusCode'),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                  },
                                  child: const Text('OK'),
                                ),
                              ],
                            );
                          },
                        );
                      }
                    }
                  },
                  child: Text('Зареєструватися'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _submitForm(String username, String email, String password, String genderAbr, String dateOfBirth) async {
    final registerUrl = Uri.parse('${url_file.myUrl}:8000/register/');
    final registerResponse = await http.post(
      registerUrl,
      body: {
        'username': username,
        'email': email,
        'password': password,
        'sex': genderAbr,
        'birthDate': dateOfBirth
      },
    );
    registrationStatusCode = registerResponse.statusCode;

    if(registrationStatusCode ==  201) {
      final data = json.decode(registerResponse.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      await prefs.setInt('id', data['user']['id']);
      await prefs.setString('username', data['user']['username']);
      await prefs.setString('email', data['user']['email']);
    }

  }
}
