import 'dart:html';

import 'package:flutter/material.dart';

void main() => runApp(
  MaterialApp(
    home: MainPage(),
  )
);


class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage>{
  @override
  Widget build (BuildContext context) => DefaultTabController(
    length: 2, 
    child: Scaffold(
      appBar: AppBar(
        title: Text("Property Hunter"),
        centerTitle: true,
        backgroundColor: Color.fromARGB(255, 38,130,166),
        bottom: TabBar(
          tabs: [
            Tab(icon: Icon(Icons.home)),
            Tab(icon: Icon(Icons.settings))
          ],
        ),
      ),
      body: TabBarView(
        children: [
          Center(child: Text('Home')),
          Center(child: Text('Settings')),
        ],
      ),
    ),
  );
}
