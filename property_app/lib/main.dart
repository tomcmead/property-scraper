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
  int currentIndex = 1;
  // final screens = [
  //   FavouritesPage(),
  //   HomePage(),
  //   SettingsPage(),
  // ];

  @override
  Widget build (BuildContext context) => Scaffold(
      appBar: AppBar(
        title: Text("Property Hunter"),
        centerTitle: true,
        backgroundColor: Color.fromARGB(255, 38,130,166),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Color.fromARGB(255, 38,130,166),
        selectedItemColor: Colors.white,
        unselectedItemColor: Colors.white70,
        currentIndex: currentIndex,
        showUnselectedLabels: false,
        showSelectedLabels: false,
        onTap: (index) => setState(() => currentIndex = index),
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite), 
            label: 'Favourites',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Settings',
          ),
        ],
      ),
    );
}
