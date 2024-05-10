import 'dart:convert';
import './constants.dart' as url_file;
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class BudgetPlanningPage extends StatefulWidget {
  @override
  _BudgetPlanningPageState createState() => _BudgetPlanningPageState();
}

class Accodomadation {
  final int id;
  final String type;
  final int amount;

  Accodomadation(
      {required this.id,
        required this.type,
        required this.amount});
}

class Transportation {
  final int id;
  final String kind;
  final int amount;

  Transportation(
      {required this.id,
        required this.kind,
        required this.amount});
}

class _BudgetPlanningPageState extends State<BudgetPlanningPage> {
  final _formKey = GlobalKey<FormState>();
  int? _income;
  Accodomadation? _accomodation;
  int? _utilities;
  int? _food;
  Transportation? _transportation;
  int? _entertainment;

  final List<Accodomadation> accomodations = [];
  final List<Transportation> transportations = [];

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token')??'';
    final url1 = Uri.parse('${url_file.myUrl}:8000/api/accomodations/');
    final response1 = await http.get(
        url1,
        headers: { 'Authorization': 'Token $token',
          'Content-Type': 'application/json'
        }
    );
    final data1 = json.decode(response1.body);

    final url2 = Uri.parse('${url_file.myUrl}:8000/api/transports/');
    final response2 = await http.get(
        url2,
        headers: { 'Authorization': 'Token $token',
          'Content-Type': 'application/json'
        }
    );
    final data2 = json.decode(response2.body);

    final List<Accodomadation> listOfAccomodations = [];
    final List<Transportation> listOfTransportations = [];
    for (int i = 0; i < data1.length; i++)
      {
        listOfAccomodations.add(Accodomadation(
            id:data1[i]['id'],
            type:data1[i]['type'],
            amount:data1[i]['amount']));
      }
    for (int i = 0; i < data2.length; i++)
    {
      listOfTransportations.add(Transportation(id:data2[i]['id'],kind:data2[i]['kind'],amount:data2[i]['amount']));
    }
    setState(() {
      accomodations.addAll(listOfAccomodations);
      transportations.addAll(listOfTransportations);
    });

    print(utf8.decode(utf8.encode(accomodations.toString())));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Розпланувати бюджет на місяць'),
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
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(labelText: 'Прибуток на місяць'),
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть прибуток';
                    }
                    return null;
                  },
                  onSaved: (value) {
                    _income = int.parse(value!);
                  },
                ),
                DropdownButtonFormField<Accodomadation>(
                  value: _accomodation,
                  items: accomodations.map((accodomadation) {
                    return DropdownMenuItem<Accodomadation>(
                      value: accodomadation,
                      child: Text(accodomadation.type),
                    );
                  }).toList(),
                  onChanged: (Accodomadation? value) {
                    setState(() {
                      _accomodation = value!;
                    });
                  },
                  validator: (value) {
                    if (value == null) {
                      return 'Будь ласка, виберіть тип житла';
                    }
                    return null;
                  },
                  decoration: InputDecoration(labelText: 'Житло'),
                ),
                TextFormField(
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(labelText: 'Комунальні послуги'),
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть витрати на комунальні послуги';
                    }
                    return null;
                  },
                  onSaved: (value) {
                    _utilities = int.parse(value!);
                  },
                ),
                TextFormField(
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(labelText: 'Їжа та продукти'),
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть витрати на їжу та продукти';
                    }
                    return null;
                  },
                  onSaved: (value) {
                    _food = int.parse(value!);
                  },
                ),
                DropdownButtonFormField<Transportation>(
                  value: _transportation,
                  items: transportations.map((transportation) {
                    return DropdownMenuItem<Transportation>(
                      value: transportation,
                      child: Text(transportation.kind),
                    );
                  }).toList(),
                  onChanged: (Transportation? value) {
                    setState(() {
                      _transportation = value!;
                    });
                  },
                  validator: (value) {
                    if (value == null) {
                      return 'Будь ласка, виберіть тип транспорта';
                    }
                    return null;
                  },
                  decoration: InputDecoration(labelText: 'Транспорт'),
                ),
                TextFormField(
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(labelText: 'Розваги та дозвілля'),
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Будь ласка, введіть витрати на розваги та дозвілля';
                    }
                    return null;
                  },
                  onSaved: (value) {
                    _entertainment = int.parse(value!);
                  },
                ),
                // Add similar fields for food, transportation, and entertainment
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      _formKey.currentState?.save();
                      // Handle budget submission
                      _submitBudget(_income!, _accomodation!, _utilities!, _food!, _transportation!, _entertainment!);
                    }
                  },
                  child: Text('Розпланувати'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _submitBudget(int income, Accodomadation accodomadation, int utilities, int food, Transportation transportation, int entertainment) {
    if(income-accodomadation.amount-transportation.amount-utilities-food-entertainment > 0){
      showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text('Вітаю!'),
            content: const Text(
                'Ви вкладаєтесь в бюджет'),
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
    } else {
      showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text('На жаль!'),
            content: const Text(
                'Ви не вкладаєтесь в бюджет'),
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
}
